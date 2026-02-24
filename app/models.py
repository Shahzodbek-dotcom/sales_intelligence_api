CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255),
    cost_price DECIMAL(10,2),
    supplier VARCHAR(255)
);

CREATE TABLE sales (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER REFERENCES products(product_id),
    category VARCHAR(50),
    price DECIMAL(10,2),
    quantity INTEGER,
    order_date DATE,
    region VARCHAR(50),
    payment_type VARCHAR(50),
    revenue DECIMAL(10,2),
    profit DECIMAL(10,2)
);

-- Indexes
CREATE INDEX idx_order_date ON sales(order_date);
CREATE INDEX idx_category ON sales(category);
CREATE INDEX idx_region ON sales(region);

-- Bonus: Materialized View for monthly revenue
CREATE MATERIALIZED VIEW monthly_revenue AS
SELECT DATE_TRUNC('month', order_date) AS month, SUM(revenue) AS total_revenue
FROM sales GROUP BY month;

-- Partitioning (order_date bo'yicha, masalan yillar bo'yicha)
CREATE TABLE sales_partitioned (LIKE sales INCLUDING ALL) PARTITION BY RANGE (order_date);