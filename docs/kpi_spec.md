## KPI Specification

### Common Filters
- Date range: `FL_DATE between start_date and end_date`
- Carrier: `AIRLINE_CODE`
- Origin airport: `ORIGIN`
- Destination airport: `DEST`

### Base Populations
- **Total flights**: all records in `silver.flights_silver` within the selected date range
- **Active flights**: records where `CANCELLED = 0 AND DIVERTED = 0`

---

### Total Flights
Business question
- How many flights occurred in the selected period?

Population
- Total flights (all records in `silver.flights_silver` within date range)

Definition / Formula
- COUNT(*) over total flights

Filters
- Optional: date range, `AIRLINE_CODE`, `ORIGIN`, `DEST`

Notes
- Includes cancelled and diverted flights unless filters restrict them.

### Active Flights
Business question
- How many flights actually operated (not cancelled or diverted)?

Population
- Active flights where `CANCELLED = 0 AND DIVERTED = 0`

Definition / Formula
- COUNT(*) over active flights

Filters
- Optional: date range, `AIRLINE_CODE`, `ORIGIN`, `DEST`

Notes
- Excludes cancelled and diverted flights by definition.

### On-time Rate
Business question
- What proportion of flights arrived on time (within 15 minutes)?

Population
- Active flights (`CANCELLED = 0 AND DIVERTED = 0`)

Definition / Formula
- On-time Rate = 100 * (COUNT_IF(ARR_DELAY <= 15) / COUNT(active flights))

Filters
- Optional: date range, `AIRLINE_CODE`, `ORIGIN`, `DEST`

Notes
- Use `ARR_DELAY` measured in minutes; exclude cancelled/diverted flights.

### Average Arrival Delay (minutes)
Business question
- What is the mean arrival delay for operating flights?

Population
- Active flights (`CANCELLED = 0 AND DIVERTED = 0`)

Definition / Formula
- AVG(ARR_DELAY) over active flights

Filters
- Optional: date range, `AIRLINE_CODE`, `ORIGIN`, `DEST`

Notes
- Negative values indicate early arrivals; exclude cancelled/diverted flights.

### Severe Delay Rate
Business question
- What share of flights experience extreme arrival delays (> 189 minutes)?

Population
- Active flights (`CANCELLED = 0 AND DIVERTED = 0`)

Definition / Formula
- Severe Delay Rate = 100 * (COUNT_IF(ARR_DELAY > 189) / COUNT(active flights))

Filters
- Optional: date range, `AIRLINE_CODE`, `ORIGIN`, `DEST`

Notes
- Threshold is p99-based; exclude cancelled/diverted flights.

### Cancellation Rate
Business question
- What proportion of scheduled flights were cancelled?

Population
- Total flights (all records in `silver.flights_silver` within date range)

Definition / Formula
- Cancellation Rate = 100 * (COUNT_IF(CANCELLED = 1) / COUNT(total flights))

Filters
- Optional: date range, `AIRLINE_CODE`, `ORIGIN`, `DEST`

Notes
- Cancelled flights are included in total population by design.

### Diversion Rate
Business question
- What proportion of scheduled flights were diverted?

Population
- Total flights (all records in `silver.flights_silver` within date range)

Definition / Formula
- Diversion Rate = 100 * (COUNT_IF(DIVERTED = 1) / COUNT(total flights))

Filters
- Optional: date range, `AIRLINE_CODE`, `ORIGIN`, `DEST`

Notes
- Diverted flights are included in total population by design.

### Top Routes by Average Delay
Business question
- Which origin-destination routes have the highest average arrival delay?

Population
- Active flights (`CANCELLED = 0 AND DIVERTED = 0`) grouped by route

Definition / Formula
- Route key: `ORIGIN || '-' || DEST`
- Metric: AVG(ARR_DELAY) per `route_key`

Filters
- Optional: date range, `AIRLINE_CODE`, `ORIGIN`, `DEST`

Notes
- Rank routes by descending AVG(ARR_DELAY); consider minimum-flight cutoffs.

### Top Carriers by Average Delay
Business question
- Which carriers have the highest average arrival delay?

Population
- Active flights (`CANCELLED = 0 AND DIVERTED = 0`) grouped by `AIRLINE_CODE`

Definition / Formula
- Metric: AVG(ARR_DELAY) per `AIRLINE_CODE`

Filters
- Optional: date range, `ORIGIN`, `DEST`, carrier filter for comparisons

Notes
- Consider excluding carriers with very few flights to avoid noise.

### Daily Trend
Business question
- How do delay metrics and on-time rates evolve day-to-day?

Population
- Active flights (`CANCELLED = 0 AND DIVERTED = 0`) grouped by `FL_DATE`

Definition / Formula
- Time series of AVG(ARR_DELAY) and/or On-time Rate per `FL_DATE`

Filters
- Optional: date range, `AIRLINE_CODE`, `ORIGIN`, `DEST`

Notes
- Use moving averages or smoothing for noisy daily series; exclude cancelled/diverted flights.
