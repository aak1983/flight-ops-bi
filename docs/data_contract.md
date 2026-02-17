## Bronze Data Contract — Mandatory Fields

The following columns are required (must not be null) because they define the minimal business identity of a flight record and enable core KPIs:

- `FL_DATE` (date): required for time-based trend analysis
- `AIRLINE_CODE` (string): required for carrier-level KPIs
- `ORIGIN` (string) and `DEST` (string): required for route-level KPIs
- `CANCELLED` (int/bool) and `DIVERTED` (int/bool): required to apply correct KPI logic

### Conditional requirement
- `ARR_DELAY` must be non-null **only for active flights** where `CANCELLED = 0` and `DIVERTED = 0`.
  Cancelled or diverted flights may legitimately have missing delay values and are handled separately in KPI logic.

## Bronze Data Contract — Mandatory Fields

These fields are required (must not be null) because they define the minimal business identity of a flight record and enable core KPIs:

- `FL_DATE` (date): required for time-based trend analysis
- `AIRLINE_CODE` (string): required for carrier-level KPIs
- `ORIGIN` (string) and `DEST` (string): required for route-level KPIs
- `CANCELLED` (int/bool) and `DIVERTED` (int/bool): required to apply correct KPI logic

### Conditional requirement (data quality rule)
- `ARR_DELAY` must be non-null for **active flights** where `CANCELLED = 0` and `DIVERTED = 0`.
  Cancelled or diverted flights may legitimately have missing delay values and are handled separately in KPI logic.
  
### Flight Key (Uniqueness)

The source dataset does not provide a single flight identifier. Therefore, an explicit `flight_key` is constructed in the bronze layer:

`flight_key = FL_DATE + AIRLINE_CODE + FL_NUMBER + ORIGIN + DEST + CRS_DEP_TIME`

This key was validated to be unique in the current dataset and is used for:
- de-duplication checks
- traceability across bronze → silver transformations
- enforcing data quality constraints (no duplicate flight records)

Note: In real-world systems, late-arriving updates may require versioning or ingestion timestamps to maintain a stable audit trail.
