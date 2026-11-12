SELECT
    COUNT(*) AS total_rows,
    SUM(customer_id IS NULL) AS missing_customer_ids,
    SUM(session_id IS NULL) AS missing_session_ids,
    SUM(revenue IS NULL) AS missing_revenue,
    COUNT(DISTINCT session_id) AS unique_sessions
FROM ecommerce_sessions;


-- Overall Business Performance

SELECT
    COUNT(*) AS total_sessions,

    SUM(purchased) AS total_purchases,

    ROUND(
        SUM(purchased) * 100.0 / COUNT(*), 2
    ) AS conversion_rate,

    ROUND(SUM(revenue), 2) AS total_revenue,

    ROUND(
        SUM(revenue) / NULLIF(SUM(purchased), 0), 2
    ) AS average_order_value,

    SUM(quantity) AS total_quantity_sold

FROM ecommerce_sessions;


-- Revenue by Product Category

SELECT
    product_category,
    COUNT(*) AS total_sessions,
    SUM(purchased) AS total_purchases,
    ROUND(SUM(revenue), 2) AS total_revenue

FROM ecommerce_sessions

GROUP BY product_category

ORDER BY total_revenue DESC;


-- Revenue by Marketing Channel

SELECT
    marketing_channel,
    COUNT(*) AS total_sessions,
    SUM(purchased) AS total_purchases,
    ROUND(SUM(revenue), 2) AS total_revenue,

    ROUND(
        SUM(purchased) * 100.0 / COUNT(*), 2
    ) AS conversion_rate

FROM ecommerce_sessions

GROUP BY marketing_channel

ORDER BY total_revenue DESC;



-- Revenue by Device Type

SELECT
    device_type,
    COUNT(*) AS total_sessions,
    SUM(purchased) AS total_purchases,
    ROUND(SUM(revenue), 2) AS total_revenue,

    ROUND(
        SUM(purchased) * 100.0 / COUNT(*), 2
    ) AS conversion_rate

FROM ecommerce_sessions

GROUP BY device_type

ORDER BY total_revenue DESC;


-- Customer Behaviour by User Type

SELECT
    user_type,
    COUNT(*) AS total_sessions,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(purchased) AS total_purchases,
    ROUND(SUM(revenue), 2) AS total_revenue,

    ROUND(
        SUM(purchased) * 100.0 / COUNT(*), 2
    ) AS conversion_rate

FROM ecommerce_sessions

GROUP BY user_type

ORDER BY total_revenue DESC;


-- Purchase Funnel Analysis

SELECT
    COUNT(*) AS total_sessions,

    SUM(added_to_cart) AS add_to_cart_sessions,

    SUM(purchased) AS purchase_sessions,

    SUM(cart_abandoned) AS abandoned_carts,

    ROUND(
        SUM(added_to_cart) * 100.0 / COUNT(*), 2
    ) AS add_to_cart_rate,

    ROUND(
        SUM(cart_abandoned) * 100.0 /
        NULLIF(SUM(added_to_cart), 0), 2
    ) AS cart_abandonment_rate

FROM ecommerce_sessions;

-- Monthly Revenue Analysis

SELECT
    visit_month,
    COUNT(*) AS total_sessions,
    SUM(purchased) AS total_purchases,
    ROUND(SUM(revenue), 2) AS total_revenue,

    ROUND(
        SUM(purchased) * 100.0 / COUNT(*), 2
    ) AS conversion_rate

FROM ecommerce_sessions

GROUP BY visit_month

ORDER BY visit_month;




-- Revenue by Weekday

SELECT
    visit_weekday,
    COUNT(*) AS total_sessions,
    SUM(purchased) AS total_purchases,
    ROUND(SUM(revenue), 2) AS total_revenue,

    ROUND(
        SUM(purchased) * 100.0 / COUNT(*), 2
    ) AS conversion_rate

FROM ecommerce_sessions

GROUP BY visit_weekday

ORDER BY total_revenue DESC;


-- Payment Method Analysis

SELECT
    payment_method,
    COUNT(*) AS total_sessions,
    SUM(purchased) AS total_purchases,
    ROUND(SUM(revenue), 2) AS total_revenue,

    ROUND(
        SUM(purchased) * 100.0 / COUNT(*), 2
    ) AS conversion_rate

FROM ecommerce_sessions

GROUP BY payment_method

ORDER BY total_revenue DESC;



-- Top 10 Customers by Revenue

SELECT
    customer_id,
    COUNT(*) AS total_sessions,
    SUM(purchased) AS total_purchases,
    ROUND(SUM(revenue), 2) AS total_revenue

FROM ecommerce_sessions

GROUP BY customer_id

ORDER BY total_revenue DESC

LIMIT 10;


-- Top 10 Products by Revenue

SELECT
    product_id,
    product_category,
    SUM(quantity) AS total_quantity_sold,
    SUM(purchased) AS total_purchases,
    ROUND(SUM(revenue), 2) AS total_revenue

FROM ecommerce_sessions

GROUP BY product_id, product_category

ORDER BY total_revenue DESC

LIMIT 10;



-- Discount Impact on Sales

SELECT
    discount_percent,
    COUNT(*) AS total_sessions,
    SUM(purchased) AS total_purchases,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(revenue), 2) AS average_revenue

FROM ecommerce_sessions

GROUP BY discount_percent

ORDER BY discount_percent;

-- Session Duration vs Purchase Behaviour

SELECT
    session_duration_bucket,
    COUNT(*) AS total_sessions,
    SUM(purchased) AS total_purchases,

    ROUND(
        SUM(purchased) * 100.0 / COUNT(*), 2
    ) AS conversion_rate,

    ROUND(SUM(revenue), 2) AS total_revenue

FROM ecommerce_sessions

GROUP BY session_duration_bucket

ORDER BY total_sessions DESC;



-- 16. Pages Viewed vs Purchases
SELECT
    pages_viewed,
    COUNT(*) AS total_sessions,
    SUM(purchased) AS total_purchases,
    ROUND(SUM(purchased) * 100.0 / COUNT(*), 2) AS conversion_rate
FROM ecommerce_sessions
GROUP BY pages_viewed
ORDER BY pages_viewed;


-- 17. Customer Ratings Analysis
SELECT
    rating,
    COUNT(*) AS total_reviews,
    ROUND(AVG(purchased) * 100, 2) AS purchase_rate,
    ROUND(AVG(revenue), 2) AS average_revenue
FROM ecommerce_sessions
WHERE rating IS NOT NULL
GROUP BY rating
ORDER BY rating DESC;


-- 18. Revenue by Location
SELECT
    location,
    COUNT(*) AS total_sessions,
    SUM(purchased) AS total_purchases,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM ecommerce_sessions
GROUP BY location
ORDER BY total_revenue DESC;


-- 19. Customer Segmentation
SELECT
    customer_id,
    COUNT(*) AS total_sessions,
    SUM(purchased) AS total_purchases,
    ROUND(SUM(revenue), 2) AS total_revenue,
    CASE
        WHEN SUM(revenue) >= 5000 THEN 'High Value'
        WHEN SUM(revenue) >= 2000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment
FROM ecommerce_sessions
GROUP BY customer_id
ORDER BY total_revenue DESC;


-- 20. Monthly Revenue Ranking using CTE and Window Function
WITH monthly_sales AS (
    SELECT
        visit_month,
        ROUND(SUM(revenue), 2) AS total_revenue
    FROM ecommerce_sessions
    GROUP BY visit_month
)
SELECT
    visit_month,
    total_revenue,
    RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank
FROM monthly_sales
ORDER BY revenue_rank;