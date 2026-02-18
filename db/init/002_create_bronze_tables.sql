-- Track pipeline runs (Bronze)
CREATE TABLE IF NOT EXISTS bronze.pipeline_runs (
    run_id uuid PRIMARY KEY,
    started_at timestamptz NOT NULL DEFAULT now(),
    finished_at timestamptz,
    status text NOT NULL CHECK (status IN ('running', 'success','failed')),
    source_file text NOT NULL,
    rows_loaded bigint NOT NULL DEFAULT 0
);


-- Raw ingestion table: keep fields as TEXT to avoid load failures.
-- Add metadata for audit/debug
CREATE TABLE IF NOT EXISTS bronze.flights_raw (
    bronze_id bigserial PRIMARY KEY,
    run_id uuid NOT NULL,
    loaded_at timestamptz NOT NULL DEFAULT now(),
    source_file text NOT NULL,

    -- Raw columns (TEXT).
    "FL_DATE" text,
    "AIRLINE_CODE" text,
    "FL_NUMBER" text,
    "ORIGIN" text,
    "DEST" text,
    "CRS_DEP_TIME" text,
    "DEP_TIME" text,
    "DEP_DELAY" text,
    "TAXI_OUT" text,
    "WHEELS_OFF" text,
    "WHEELS_ON" text,
    "TAXI_IN" text,
    "CRS_ARR_TIME" text,
    "ARR_TIME" text,
    "ARR_DELAY" text,
    "CANCELLED" text,
    "CANCELLATION_CODE" text,
    "DIVERTED" text,
    "AIR_TIME" text,
    "DISTANCE" text,
    "CARRIER_DELAY" text,
    "WEATHER_DELAY" text,
    "NAS_DELAY" text,
    "SECURITY_DELAY" text,
    "LATE_AIRCRAFT_DELAY" text,

    CONSTRAINT fk_bronze_flights_raw_run
      FOREIGN KEY (run_id)
      REFERENCES bronze.pipeline_runs (run_id)
);

CREATE INDEX IF NOT EXISTS idx_bronze_flights_raw_run_id ON bronze.flights_raw(run_id);
CREATE INDEX IF NOT EXISTS idx_bronze_flights_raw_loaded_at ON bronze.flights_raw(loaded_at);

