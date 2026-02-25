CREATE TABLE products_data (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    cost_price NUMERIC(10, 2) NOT NULL,
    supplier VARCHAR(255)
);

CREATE TABLE sales_data (
    order_id VARCHAR(50),
    customer_id VARCHAR(50),
    product_id VARCHAR(50) REFERENCES products(product_id),
    category VARCHAR(100),
    price NUMERIC(10, 2),
    quantity INTEGER,
    order_date DATE,
    region VARCHAR(100),
    payment_type VARCHAR(50),
    revenue NUMERIC(10, 2),
    profit NUMERIC(10, 2),
    PRIMARY KEY (order_id, order_date)
) PARTITION BY RANGE (order_date);


CREATE TABLE sales_intelligence_api PARTITION OF sales FOR VALUES FROM ('2024-01-01') TO ('2025-12-31');

CREATE INDEX idx_sales_product_id ON sales(product_id);
CREATE INDEX idx_sales_order_date ON sales(order_date);
CREATE INDEX idx_sales_region ON sales(region);


CREATE MATERIALIZED VIEW monthly_sales_summary AS
SELECT 
    DATE_TRUNC('month', order_date) as month,
    SUM(revenue) as total_revenue,
    SUM(profit) as total_profit
FROM sales
GROUP BY 1;