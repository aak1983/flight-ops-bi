## Silver Layer Specification

### Purpose
The silver layer enforces data quality rules and business logic to produce analytics-ready flight records for KPI computation and dashboard consumption.

### Record Inclusion
- A record is included in `silver.flights_silver` if:
- All mandatory bronze fields are present (`FL_DATE`, `AIRLINE_CODE`, `ORIGIN`, `DEST`, `CANCELLED`, `DIVERTED`)
- `ARR_DELAY` is present for active flights (`CANCELLED=0` and `DIVERTED=0`)
- `flight_key` is unique
- Airport codes are valid IATA format (3 uppercase letters)
- `CANCELLED` and `DIVERTED` are valid boolean indicators (0/1)
- Delay values pass engineering guardrails (no impossible values)

### Warning Flags (records are kept but flagged)
The following conditions are flagged as warnings:
- Severe delays: `ARR_DELAY > 189` minutes (p99-based)
- Extreme delays: `ARR_DELAY > 643` minutes (p999-based)
- Very early arrivals: `ARR_DELAY < -60` minutes

- ### Derived Columns
- The silver layer adds the following derived fields:
- `flight_key`: constructed unique identifier
- `route_key`: `ORIGIN || '-' || DEST`
- `is_active_flight`: `(CANCELLED=0 AND DIVERTED=0)`
- `is_ontime`: `is_active_flight AND ARR_DELAY <= 15`
- `delay_bucket`: {Early, On-time, Minor, Major, Severe}
- `dq_status`: PASS/WARN
- `dq_flags`: pipe-separated warning flags (e.g., `SEVERE_DELAY|EARLY_ARRIVAL`)

### Quality Reporting
Each pipeline run writes summary metrics to `pipeline_runs` and rule-level events to `quality_issues` to support monitoring and auditing.
