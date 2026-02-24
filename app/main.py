from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any

# Analytics va forecasting modullarni import qilamiz
from .analytics import (
    get_total_revenue,
    get_total_profit,
    get_profit_margin,
    get_top_10_products,
    get_most_profitable_category,
    get_lowest_region,
    get_monthly_revenue_trend,
    get_weekday_vs_weekend,
    get_payment_distribution,
    load_cleaned_data
)
from .forecasting import forecast_next_month_revenue

app = FastAPI(
    title="Sales Intelligence API",
    description="Sales data analysis and forecasting API for business insights",
    version="1.0.0"
)

# Global df (productionda yaxshiroq caching/DB ishlatiladi)
try:
    df_global = load_cleaned_data()
except FileNotFoundError:
    df_global = pd.DataFrame()  # Agar cleaned file yo'q bo'lsa


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Sales Intelligence API ishlamoqda",
        "docs": "/docs",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


@app.get("/metrics", response_model=Dict[str, Any], tags=["Metrics"])
def metrics():
    """
    Asosiy biznes metrikalari:
    - Total revenue
    - Total profit
    - Profit margin (%)
    """
    if df_global.empty:
        raise HTTPException(status_code=503, detail="Cleaned data hali yuklanmagan. Avval data_pipeline.py ni ishga tushiring.")

    return {
        "total_revenue": round(get_total_revenue(), 2),
        "total_profit": round(get_total_profit(), 2),
        "profit_margin_percent": get_profit_margin()
    }


@app.get("/top-products", response_model=List[Dict[str, Any]], tags=["Performance"])
def top_products(limit: int = 10):
    """
    Revenue bo'yicha top mahsulotlar (default 10 ta)
    """
    if df_global.empty:
        raise HTTPException(status_code=503, detail="Data mavjud emas")

    top_list = get_top_10_products()
    return top_list[:limit]  # limit parametri bilan cheklash mumkin


@app.get("/sales-trend", response_model=Dict[str, Any], tags=["Trends"])
def sales_trend():
    """
    Trendlar:
    - Monthly revenue trend
    - Weekday vs Weekend sales
    - Payment type distribution (%)
    """
    if df_global.empty:
        raise HTTPException(status_code=503, detail="Data mavjud emas")

    return {
        "monthly_revenue_trend": get_monthly_revenue_trend(),
        "weekday_vs_weekend": get_weekday_vs_weekend(),
        "payment_distribution_percent": get_payment_distribution()
    }


@app.get("/region-performance", response_model=Dict[str, Any], tags=["Performance"])
def region_performance():
    """
    Eng foydali kategoriya va eng past profitli region
    """
    if df_global.empty:
        raise HTTPException(status_code=503, detail="Data mavjud emas")

    best_cat, best_profit = get_most_profitable_category()
    worst_region, worst_profit = get_lowest_region()

    return {
        "most_profitable_category": {
            "category": best_cat,
            "total_profit": round(best_profit, 2)
        },
        "lowest_performance_region": {
            "region": worst_region,
            "total_profit": round(worst_profit, 2)
        }
    }


@app.get("/forecast", response_model=Dict[str, Any], tags=["Forecasting"])
def forecast():
    """
    Kelasi oy uchun revenue prognozi (3 oylik moving average asosida)
    """
    if df_global.empty:
        raise HTTPException(status_code=503, detail="Data mavjud emas")

    predicted = forecast_next_month_revenue()  # ← () qo'shildi!

    return {
        "next_month_revenue": round(predicted, 2),
        "method": "3-month moving average",
        "note": "Oxirgi 3 oy o'rtachasi asosida hisoblandi"
    }