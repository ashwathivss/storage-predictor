import pandas as pd

CAPACITY_GB = 10          # set your disk or table limit here
THRESHOLD = 0.8           # warn at 80% of capacity
CAPACITY_BYTES = CAPACITY_GB * 1e9

fc = pd.read_csv("data/forecast.csv", parse_dates=["date"])

print(f"Capacity: {CAPACITY_GB} GB, alert at {THRESHOLD*100:.0f}%\n")

for name, group in fc.groupby("table_name"):
    group = group.sort_values("date")
    limit = CAPACITY_BYTES * THRESHOLD
    crossed = group[group["upper"] > limit]

    if crossed.empty:
        print(f"OK     {name}: stays under limit for 90 days "
              f"(day +90 upper: {group['upper'].iloc[-1]/1e9:.2f} GB)")
    else:
        first = crossed.iloc[0]
        if first["days_ahead"] == 1:
            print(f"OVER   {name}: already above limit "
                  f"(upper {first['upper']/1e9:.2f} GB)")
        else:
            print(f"ALERT  {name}: crosses limit on {first['date'].date()} "
                  f"(day +{first['days_ahead']}, upper {first['upper']/1e9:.2f} GB)")