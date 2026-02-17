## Data Quality Rules — Thresholds (Derived from Data)

### Distribution summary (ARR_DELAY)
- Q1 = -16, Median = -7, Q3 = 7
- p90 = 36, p95 = 71, p99 = 189, p999 = 643
- min = -96, max = 2934

### Rules

| Rule ID | Description | Severity | Threshold Source | Action |
|--------|-------------|----------|------------------|--------|
| R001 | Mandatory fields must not be null (`FL_DATE`, `AIRLINE_CODE`, `ORIGIN`, `DEST`, `CANCELLED`, `DIVERTED`) | ERROR | data contract | Reject record |
| R002 | `ARR_DELAY` must be non-null for active flights (`CANCELLED=0` and `DIVERTED=0`) | ERROR | data contract | Reject record |
| R003 | `flight_key` must be unique | ERROR | design constraint | Reject duplicates / fail run |
| R004 | Airport codes must be valid IATA format (3 uppercase letters) for `ORIGIN` and `DEST` | ERROR | business rule | Reject record |
| R005 | `CANCELLED` and `DIVERTED` must be 0/1 | ERROR | business rule | Reject record |
| R006 | Severe arrival delays should be flagged (`ARR_DELAY > 189` minutes) | WARNING | p99(ARR_DELAY)=189 | Keep + flag |
| R007 | Extreme arrival delays should be flagged (`ARR_DELAY > 643` minutes) | WARNING | p999(ARR_DELAY)=643 | Keep + flag |
| R008 | Very early arrivals should be flagged (`ARR_DELAY < -60` minutes) | WARNING | chosen using observed min=-96 | Keep + flag |
| R009 | Guardrail: impossible delay values should be rejected (`ARR_DELAY > 10000` or `ARR_DELAY < -1000`) | ERROR | engineering guardrail | Reject record |
