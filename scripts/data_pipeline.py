import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    try:
        sales = pd.read_csv('data/sales_data.csv')
        products = pd.read_csv('data/products_data.csv')

        # Merge cost_price ni olish uchun
        merged = sales.merge(
            products[['product_id', 'cost_price', 'product_name']],
            on='product_id',
            how='left'
        )

        # Missing values va duplicates tozalash
        merged.drop_duplicates(inplace=True)
        merged.dropna(subset=['price', 'quantity', 'cost_price', 'order_date'], inplace=True)

        # Noto‘g‘ri narx yoki quantity aniqlash
        merged = merged[(merged['price'] > 0) & (merged['quantity'] > 0)]

        # Sanalarni normalize qilish
        merged['order_date'] = pd.to_datetime(merged['order_date'], errors='coerce')
        merged.dropna(subset=['order_date'], inplace=True)

        # Revenue,Profit hisoblash
        merged['revenue'] = merged['price'] * merged['quantity']
        merged['profit'] = (merged['price'] - merged['cost_price']) * merged['quantity']

        # Saqlash
        merged.to_csv('data/cleaned_sales.csv', index=False)
        logging.info(f"Pipeline muvaffaqiyatli yakunlandi. Cleaned data shape: {merged.shape}")
        logging.info(f"Total revenue (sample): {merged['revenue'].sum():,.2f}")
        logging.info(f"Total profit (sample): {merged['profit'].sum():,.2f}")

    except Exception as e:
        logging.error(f"Xato yuz berdi: {e}")

if __name__ == "__main__":
    run_pipeline()