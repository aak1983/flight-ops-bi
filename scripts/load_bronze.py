import argparse
from datetime import datetime, timezone
import os
import uuid
from dotenv import load_dotenv
import psycopg2


load_dotenv()

RAW_COLUMNS = [
    "FL_DATE",
    "AIRLINE",
    "AIRLINE_DOT",
    "AIRLINE_CODE",
    "DOT_CODE",
    "FL_NUMBER",
    "ORIGIN",
    "ORIGIN_CITY",
    "DEST",
    "DEST_CITY",
    "CRS_DEP_TIME",
    "DEP_TIME",
    "DEP_DELAY",
    "TAXI_OUT",
    "WHEELS_OFF",
    "WHEELS_ON",
    "TAXI_IN",
    "CRS_ARR_TIME",
    "ARR_TIME",
    "ARR_DELAY",
    "CANCELLED",
    "CANCELLATION_CODE",
    "DIVERTED",
    "CRS_ELAPSED_TIME",
    "ELAPSED_TIME",
    "AIR_TIME",
    "DISTANCE",
    "DELAY_DUE_CARRIER",
    "DELAY_DUE_WEATHER",
    "DELAY_DUE_NAS",
    "DELAY_DUE_SECURITY",
    "DELAY_DUE_LATE_AIRCRAFT",
]

def get_conn():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=int(os.getenv("PGPORT", "5432")),
        dbname=os.getenv("PGUSER", "flightops"),
        user=os.getenv("PGUSER", "flightops"),
        password=os.getenv("PGPASSWORD", "flightops"),
    )
    
def create_run(cur: psycopg2.extensions.cursor, run_id, source_file):
    cur.execute(
        """
        INSERT INTO bronze.pipeline_runs (run_id, status, source_file)
        VALUES (%s, 'running', %s)
        """,
        (str(run_id), source_file),
    )
    
def finish_run_success(cur, run_id, rows_loaded):
    cur.execute(
        """
        UPDATE bronze.pipeline_runs
        SET status='success', finished_at=now(), rows_loaded=%s
        WHERE run_id=%s
        """,
        (rows_loaded, str(run_id)),
    )

def finish_run_failed(cur, run_id, err):
    cur.execute(
        """
        UPDATE bronze.pipeline_runs
        SET status='failed', finished_atnow(), error_message=%s
        WHERE run_id=%sw
        """,
        (str(err)[:5000], str(run_id)),
    )
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to flights CSV file")
    parser.add_argument("--source_file", default=None, help="Value to store in source_file (default to CSV filename)")
    args = parser.parse_args()
    
    csv_path = args.csv
    source_file = args.source_file or os.path.basename(csv_path)
    
    run_id = uuid.uuid4()
    loaded_at = datetime.now(timezone.utc)
    
    conn = get_conn()
    conn.autocommit = False
    
    try:
        with conn.cursor() as cur:
            create_run(cur, run_id, source_file)
            
            # Temp table to COPY raw columns only (no metadata)
            temp_table = f"rmp_flights_raw_{run_id.hex}"
            cur.execute(f"CREATE TEMP TABLE {temp_table} (LIKE bronze.flights_raw INCLUDING DEFAULTS) ON COMMIT DROP;")
            # Drop metadata + identity from temp (keep only raw columns)
            cur.execute(f"ALTER TABLE {temp_table} DROP COLUMN bronze_id;")
            cur.execute(f"ALTER TABLE {temp_table} DROP COLUMN run_id;")
            cur.execute(f"ALTER TABLE {temp_table} DROP COLUMN loaded_at")
            cur.execute(f"ALTER TABLE {temp_table} DROP COLUMN source_file")

            # COPY into temp
            cols_sql = ", ".join(RAW_COLUMNS)
            copy_sql = f"COPY {temp_table} ({cols_sql}) FROM STDIN WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '\"')"
            with open(csv_path, "r", encoding="utf-8") as f:
                cur.copy_expert(copy_sql, f)
            
            # Insert into bronze with metadata
            insert_sql = f"""
                INSERT INTO bronze.flights_raw (
                    run_id, loaded_at, source_file, {cols_sql}
                )
                SELECT
                    %s, %s, %s, {cols_sql}
                FROM {temp_table}
            """
            cur.execute(insert_sql, (str(run_id), loaded_at, source_file))
            
            # Count rows inserted for this run
            cur.execute("SELECT COUNT(*) FROM bronze.flights_raw WHERE run_id=%s", (str(run_id),))
            rows_loaded = cur.fetchone()[0]
            
            finish_run_success(cur, run_id, rows_loaded)
            
        conn.commit()
        
        print(f"OK: run_id={run_id} rows_loaded={rows_loaded}, source_file={source_file}")
        
    except Exception as e:
        conn.rollback()
        try:
            with conn.cursor() as cur:
                finish_run_failed(cur, run_id, e)
            conn.commit()
        except Exception:
            pass
        raise
    finally:
        conn.close()
        
if __name__ == '__main__':
    main()
            
            
            
            
    