# Predictive Database Storage Management

Forecasts table size 90 days ahead with Prophet and LinearRegression, and warns when capacity is near.

## Run it
pip install pandas scikit-learn prophet streamlit matplotlib
python generate_data.py
python forecast.py
python predict_future.py
python alerts.py
python -m streamlit run app.py