import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/history.csv", parse_dates=["date"])

fig, ax = plt.subplots(figsize=(10, 5))
for name, group in df.groupby("table_name"):
    ax.plot(group["date"], group["size_bytes"] / 1e9, label=name)

ax.set_title("Table size over time")
ax.set_ylabel("Size (GB)")
ax.set_xlabel("Date")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("data/explore.png", dpi=120)
plt.show()
print("Saved data/explore.png")