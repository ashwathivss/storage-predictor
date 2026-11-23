import os
import numpy as np
import pandas as pd

np.random.seed(42)  # same fake data every run

DAYS = 180
START = pd.Timestamp("2026-01-01")

# three fake tables: name, starting size (bytes), daily growth (bytes)
TABLES = {
    "orders":    {"start": 2_000_000_000, "growth": 15_000_000},
    "customers": {"start": 800_000_000,   "growth": 4_000_000},
    "logs":      {"start": 3_000_000_000, "growth": 30_000_000},
}

rows = []
for name, cfg in TABLES.items():
    for day in range(DAYS):
        trend = cfg["start"] + cfg["growth"] * day
        noise = np.random.normal(0, cfg["growth"] * 2)
        spike = 500_000_000 if (name == "logs" and day == 120) else 0  # one batch-job spike
        size = int(trend + noise + spike)
        rows.append({
            "table_name": name,
            "date": (START + pd.Timedelta(days=day)).date(),
            "size_bytes": size,
        })

os.makedirs("data", exist_ok=True)
df = pd.DataFrame(rows)
df.to_csv("data/history.csv", index=False)
print(f"Saved {len(df)} rows to data/history.csv")