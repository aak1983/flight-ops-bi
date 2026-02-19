-- Track pipeline runs (Bronze)
create table if not exists bronze.pipeline_runs (
   run_id      uuid primary key,
   started_at  timestamptz not null default now(),
   finished_at timestamptz,
   status      text not null check ( status in ( 'running',
                                            'success',
                                            'failed' ) ),
   source_file text not null,
   rows_loaded bigint not null default 0
);


-- Raw ingestion table: keep fields as TEXT to avoid load failures.
-- Add metadata for audit/debug
create table if not exists bronze.flights_raw (
   bronze_id               bigserial primary key,
   run_id                  uuid not null,
   loaded_at               timestamptz not null default now(),
   source_file             text not null,

    -- Raw columns (TEXT).
   fl_date                 text,
   airline                 text,
   airline_dot             text,
   airline_code            text,
   dot_code                text,
   fl_number               text,
   origin                  text,
   origin_city             text,
   dest                    text,
   dest_city               text,
   crs_dep_time            text,
   dep_time                text,
   dep_delay               text,
   taxi_out                text,
   wheels_off              text,
   wheels_on               text,
   taxi_in                 text,
   crs_arr_time            text,
   arr_time                text,
   arr_delay               text,
   cancelled               text,
   cancellation_code       text,
   diverted                text,
   crs_elapsed_time        text,
   elapsed_time            text,
   air_time                text,
   distance                text,
   delay_due_carrier       text,
   delay_due_weather       text,
   delay_due_nas           text,
   delay_due_security      text,
   delay_due_late_aircraft text,
   constraint fk_bronze_flights_raw_run foreign key ( run_id )
      references bronze.pipeline_runs ( run_id )
);

create index if not exists idx_bronze_flights_raw_run_id on
   bronze.flights_raw (
      run_id
   );
create index if not exists idx_bronze_flights_raw_loaded_at on
   bronze.flights_raw (
      loaded_at
   );