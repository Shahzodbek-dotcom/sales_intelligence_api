import pandas as pd

def load_cleaned_data():
    """Har safar yangi yuklamaslik uchun cache qilish mumkin (keyinchalik)"""
    return pd.read_csv('data/cleaned_sales.csv', parse_dates=['order_date'])

df_global = load_cleaned_data()  # Global uchun (test uchun oddiy, productionda yaxshiroq qilamiz)

def get_total_revenue():
    return float(df_global['revenue'].sum())

def get_total_profit():
    return float(df_global['profit'].sum())

def get_profit_margin():
    rev = get_total_revenue()
    return round((get_total_profit() / rev * 100), 2) if rev > 0 else 0.0

def get_top_10_products():
    grouped = df_global.groupby(['product_id', 'product_name'])['revenue'].sum().reset_index()
    top = grouped.nlargest(10, 'revenue')
    return top[['product_id', 'product_name', 'revenue']].to_dict(orient='records')

def get_most_profitable_category():
    grouped = df_global.groupby('category')['profit'].sum()
    return grouped.idxmax(), float(grouped.max())

def get_lowest_region():
    grouped = df_global.groupby('region')['profit'].sum()
    return grouped.idxmin(), float(grouped.min())

def get_monthly_revenue_trend():
    df_global['month'] = df_global['order_date'].dt.to_period('M')
    trend = df_global.groupby('month')['revenue'].sum().reset_index()
    trend['month'] = trend['month'].astype(str)
    return trend.to_dict(orient='records')

def get_weekday_vs_weekend():
    df_global['is_weekend'] = df_global['order_date'].dt.weekday >= 5
    grouped = df_global.groupby('is_weekend')['revenue'].sum()
    return {
        "weekday": float(grouped.get(False, 0)),
        "weekend": float(grouped.get(True, 0))
    }

def get_payment_distribution():
    dist = df_global['payment_type'].value_counts(normalize=True) * 100
    return {k: round(v, 2) for k, v in dist.items()}