import pandas as pd

def forecast_next_month_revenue():
    df = load_cleaned_data()
    df['month'] = df['order_date'].dt.to_period('M')
    monthly = df.groupby('month')['revenue'].sum().sort_index()
    
    if len(monthly) < 3:
        return float(monthly.mean())
    
    # 3 oylik moving average
    ma = monthly.rolling(window=3).mean().iloc[-1]
    return float(ma)