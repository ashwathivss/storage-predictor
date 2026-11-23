# Predictive Database Storage Management

## 1. Problem
Databases grow over time. Running out of disk causes outages. This project uses machine learning to forecast table size 90 days ahead and warn before capacity is reached.

## 2. Data
- Synthetic history: 3 tables (orders, customers, logs), 180 days each, 540 rows.
- Columns: table_name, date, size_bytes.
- Logs includes one batch-job spike on day 120.
- Limitation: data is generated, not from a real database.

## 3. Models
- Baseline: LinearRegression on day number.
- ML model: Prophet (trend-based time series model).
- Test: train on days 1-150, predict days 151-180. Metric: MAPE.

## 4. Results
| Table | LinearRegression MAPE | Prophet MAPE | Best |
|---|---|---|---|
| customers | 0.35% | 0.48% | LinearRegression |
| logs | 0.52% | 0.51% | Prophet (near tie) |
| orders | 0.52% | 0.56% | LinearRegression |

Simple models did as well as Prophet on this clean data.

## 5. Forecast (90 days ahead, Prophet)
- customers: 1.63 GB at +30, 1.86 GB at +90
- orders: 5.16 GB at +30, 6.09 GB at +90
- logs: 9.21 GB at +30, 10.96 GB at +90

## 6. Alerts
Capacity set to 10 GB, alert at 80% (8 GB).
- logs: already above limit (OVER).
- orders, customers: OK for 90 days.

## 7. Dashboard
Streamlit app shows actual history, prediction, and upper/lower bounds per table, plus alert status.

## 8. Limitations
- Synthetic data, smooth and low noise.
- Short history (180 days).
- Single spike; model cannot predict future spikes.
- Bounds are narrow, which real data would not produce.

## 9. Future work
- Use real database metrics.
- Test LightGBM for spiky tables.
- Connect alerts to Slack or email.