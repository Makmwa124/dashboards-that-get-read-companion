-- Chapter 12: why the dashboard and the finance pack disagreed
SELECT ROUND(SUM(revenue), 0)                    AS before_returns,
       ROUND(SUM(revenue * (returned = 1)), 0)   AS returned,
       ROUND(SUM(revenue * (returned = 0)), 0)   AS net_of_returns,
       ROUND(SUM(revenue) * 1.1, 0)              AS incl_gst
FROM orders
WHERE order_date BETWEEN '2025-07-01' AND '2026-06-30';
