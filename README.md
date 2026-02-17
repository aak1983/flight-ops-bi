## Data Understanding & Assumptions

This project uses a flight delay dataset representing operational flight records.

### Key Assumptions

- A logical flight identifier is constructed using:
  `FL_DATE + AIRLINE_CODE + FL_NUMBER + ORIGIN + DEST`
- Arrival delay (`ARR_DELAY`) is used as the primary performance metric, as it best reflects passenger experience.
- Flights marked as `CANCELLED = 1` are excluded from delay-based KPIs.
- On-time performance is defined as `ARR_DELAY <= 15 minutes`, following common industry practice.

### Data Layers

- **Bronze**: Minimal transformation layer preserving raw data with standardized naming and data types.
- **Silver**: Data quality rules applied and business logic enforced.
- **Gold**: Analytics-ready views exposing KPIs for dashboard consumption.

This project follows the Medallion architecture (Bronze, Silver, Gold) commonly used in Databricks Lakehouse environments.
