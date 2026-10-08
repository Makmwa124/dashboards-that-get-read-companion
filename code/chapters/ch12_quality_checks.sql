-- Chapter 12: freshness and quality checks to run before every refresh
-- 1. How fresh is the data?
SELECT MAX(order_date) AS latest_order,
       COUNT(*)        AS total_rows
FROM orders;

-- 2. Did every month and region load?
SELECT substr(order_date, 1, 7) AS month,
       COUNT(DISTINCT region)   AS regions,
       COUNT(*)                 AS orders
FROM orders
WHERE order_date >= '2026-01-01'
GROUP BY month
ORDER BY month;

-- 3. Rows that break business rules
SELECT SUM(revenue <= 0)        AS non_positive_revenue,
       SUM(cost > revenue)      AS cost_above_revenue,
       SUM(order_id IS NULL)    AS missing_id,
       COUNT(*) - COUNT(DISTINCT order_id) AS duplicate_ids
FROM orders;

-- 4. Does the dashboard total reconcile to the source?
SELECT ROUND(SUM(revenue), 2) AS fy26_revenue
FROM orders
WHERE order_date BETWEEN '2025-07-01' AND '2026-06-30';
