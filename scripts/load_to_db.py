# scripts/load_to_db.py
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import logging

# Logging sozlash (xatolarni ko'rish uchun)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# .env fayldan o'qish
load_dotenv()

DATABASE_URL = os.getenv("postgresql://localhost:5432/analyze_db")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL .env faylda topilmadi! .env ga quyidagini qo'shing:\nDATABASE_URL=postgresql://postgres:PAROLINGIZ@localhost:5432/sales_intelligence")

logging.info(f"Ulanyapman: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    logging.info("Engine muvaffaqiyatli yaratildi")
except Exception as e:
    logging.error(f"Engine yaratishda xato: {e}")
    raise

def load_data():
    try:
        # Tozalangan data ni o'qish
        df = pd.read_csv('data/cleaned_sales.csv')
        logging.info(f"cleaned_sales.csv o'qildi: {df.shape[0]:,} qator")

        # 1. Products jadvali (takrorlanmas qilish)
        products_df = df[['product_id', 'product_name', 'category', 'cost_price']] \
                        .drop_duplicates(subset=['product_id'])
        products_df.to_sql('products', engine, if_exists='replace', index=False)
        logging.info(f"products jadvaliga {len(products_df)} ta mahsulot yuklandi")

        # 2. Sales jadvali (katta bo'lgani uchun chunks bilan)
        df.to_sql('sales', engine, if_exists='replace', index=False, chunksize=10000)
        logging.info(f"sales jadvaliga {len(df):,} ta buyurtma yuklandi")

        logging.info("Ma'lumotlar bazaga muvaffaqiyatli yuklandi!")

    except FileNotFoundError as e:
        logging.error(f"Fayl topilmadi: {e}")
    except Exception as e:
        logging.error(f"Boshqa xato: {e}")
        raise

if __name__ == "__main__":
    load_data()