USE ecommerce_bi;

SELECT DATABASE();

SHOW TABLES;

CREATE TABLE ecommerce_sessions (
    customer_id INT,
    session_id INT,
    visit_date DATE,
    device_type VARCHAR(50),
    user_type VARCHAR(50),
    marketing_channel VARCHAR(100),
    product_id INT,
    product_category VARCHAR(100),
    unit_price DECIMAL(10,2),
    quantity INT,
    discount_percent DECIMAL(5,2),
    discount_amount DECIMAL(10,2),
    revenue DECIMAL(12,2),
    pages_viewed INT,
    time_on_site_sec INT,
    added_to_cart TINYINT,
    purchased TINYINT,
    cart_abandoned TINYINT,
    rating DECIMAL(3,2),
    review_text VARCHAR(255),
    review_helpful_votes INT,
    payment_method VARCHAR(50),
    visit_day INT,
    visit_month INT,
    visit_weekday VARCHAR(30),
    visit_season VARCHAR(30),
    session_duration_bucket VARCHAR(50),
    revenue_normalized DECIMAL(12,6),
    location VARCHAR(100)
);

USE ecommerce_bi;

SHOW TABLES;

DESCRIBE ecommerce_sessions;

SHOW VARIABLES LIKE 'local_infile';

SELECT COUNT(*) FROM ecommerce_sessions;

SELECT *
FROM ecommerce_sessions
LIMIT 10;

SELECT
    COUNT(*) AS total_rows,
    SUM(customer_id IS NULL) AS missing_customer_ids,
    SUM(session_id IS NULL) AS missing_session_ids,
    SUM(revenue IS NULL) AS missing_revenue,
    COUNT(DISTINCT session_id) AS unique_sessions
FROM ecommerce_sessions;