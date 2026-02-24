# app/forecasting.py
import pandas as pd
from .analytics import load_cleaned_data     # ← BU QATORNI QO‘SHING!


def forecast_next_month_revenue():
    df = load_cleaned_data()
    
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df = df.dropna(subset=['order_date', 'revenue'])

    if df.empty:
        return 0.0

    df['month'] = df['order_date'].dt.to_period('M')
    monthly = df.groupby('month')['revenue'].sum().sort_index()

    if len(monthly) == 0:
        return 0.0
    
    if len(monthly) < 3:
        return float(monthly.mean() or 0.0)

    ma = monthly.rolling(window=3, min_periods=1).mean().iloc[-1]
    return float(ma)