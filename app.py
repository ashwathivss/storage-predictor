import pandas as pd
import streamlit as st

CAPACITY_GB = 10
THRESHOLD = 0.8
LIMIT_BYTES = CAPACITY_GB * 1e9 * THRESHOLD

st.set_page_config(page_title="Storage Predictor", layout="wide")
st.title("Database Storage Predictor")

history = pd.read_csv("data/history.csv", parse_dates=["date"])
forecast = pd.read_csv("data/forecast.csv", parse_dates=["date"])

tables = sorted(history["table_name"].unique())
choice = st.selectbox("Table", tables)

h = history[history["table_name"] == choice].set_index("date")["size_bytes"] / 1e9
f = forecast[forecast["table_name"] == choice].set_index("date")

# one chart: actual history, predicted, and the upper bound band
chart = pd.DataFrame({
    "Actual (GB)": h,
    "Predicted (GB)": f["predicted"] / 1e9,
    "Upper bound (GB)": f["upper"] / 1e9,
    "Lower bound (GB)": f["lower"] / 1e9,
})
st.line_chart(chart)

st.subheader("Alert status")
over = (f["upper"] > LIMIT_BYTES)
if over.any():
    first = f[over].iloc[0]
    st.warning(f"Upper bound crosses {CAPACITY_GB * THRESHOLD:.0f} GB limit on "
               f"{first.name.date()} (day +{first['days_ahead']}).")
else:
    st.success("Stays under limit for 90 days.")

st.subheader("All tables")
summary = []
for name in tables:
    ff = forecast[forecast["table_name"] == name]
    peak = ff["upper"].max() / 1e9
    summary.append({"table": name, "day +90 upper (GB)": round(ff["upper"].iloc[-1] / 1e9, 2),
                    "status": "ALERT" if peak > CAPACITY_GB * THRESHOLD else "OK"})
st.dataframe(pd.DataFrame(summary), hide_index=True)