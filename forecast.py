import logging
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from prophet import Prophet

# hide Prophet's chatty log output
logging.getLogger("prophet").setLevel(logging.WARNING)
logging.getLogger("cmdstanpy").setLevel(logging.WARNING)

TRAIN_DAYS = 150

df = pd.read_csv("data/history.csv", parse_dates=["date"])

def mape(actual, predicted):
    return np.mean(np.abs((actual - predicted) / actual)) * 100

for name, group in df.groupby("table_name"):
    group = group.sort_values("date").reset_index(drop=True)
    group["day"] = np.arange(len(group))

    train = group[group["day"] < TRAIN_DAYS]
    test = group[group["day"] >= TRAIN_DAYS]
    actual = test["size_bytes"].values

    # Model 1: LinearRegression (baseline)
    lr = LinearRegression()
    lr.fit(train[["day"]], train["size_bytes"])
    lr_pred = lr.predict(test[["day"]])

    # Model 2: Prophet (ML)
    prophet_train = train[["date", "size_bytes"]].rename(columns={"date": "ds", "size_bytes": "y"})
    m = Prophet(daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=False)
    m.fit(prophet_train)
    future = pd.DataFrame({"ds": test["date"].values})
    prophet_pred = m.predict(future)["yhat"].values

    lr_err = mape(actual, lr_pred)
    prophet_err = mape(actual, prophet_pred)
    winner = "Prophet" if prophet_err < lr_err else "LinearRegression"

    print(f"{name}: LinearRegression {lr_err:.2f}% | Prophet {prophet_err:.2f}% | best: {winner}")