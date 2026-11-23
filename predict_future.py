import logging
import pandas as pd
from prophet import Prophet

logging.getLogger("prophet").setLevel(logging.WARNING)
logging.getLogger("cmdstanpy").setLevel(logging.WARNING)

HORIZON = 90  # days ahead

df = pd.read_csv("data/history.csv", parse_dates=["date"])
results = []

for name, group in df.groupby("table_name"):
    group = group.sort_values("date")
    train = group[["date", "size_bytes"]].rename(columns={"date": "ds", "size_bytes": "y"})

    m = Prophet(daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=False)
    m.fit(train)

    future = m.make_future_dataframe(periods=HORIZON)
    fc = m.predict(future)
    fc = fc[fc["ds"] > train["ds"].max()].copy()  # keep only future days
    fc["table_name"] = name
    fc["days_ahead"] = range(1, HORIZON + 1)
    results.append(fc[["table_name", "ds", "days_ahead", "yhat", "yhat_lower", "yhat_upper"]])

out = pd.concat(results).rename(columns={
    "ds": "date", "yhat": "predicted", "yhat_lower": "lower", "yhat_upper": "upper",
})
for col in ["predicted", "lower", "upper"]:
    out[col] = out[col].round(0).astype("int64")

out.to_csv("data/forecast.csv", index=False)
print(f"Saved {len(out)} rows to data/forecast.csv")

# quick look at the 30, 60, 90 day marks
for name in out["table_name"].unique():
    rows = out[(out["table_name"] == name) & (out["days_ahead"].isin([30, 60, 90]))]
    for _, r in rows.iterrows():
        print(f"{name} day +{r['days_ahead']}: {r['predicted']/1e9:.2f} GB (upper {r['upper']/1e9:.2f} GB)")