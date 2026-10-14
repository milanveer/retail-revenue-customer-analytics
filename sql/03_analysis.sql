-- 1. Data quality checks (expect 541909 rows if full UCI dataset was imported).
SELECT COUNT(*) AS total_rows,
 COUNT(*) FILTER (WHERE invoice_no IS NULL OR invoice_date IS NULL OR quantity IS NULL OR unit_price IS NULL) AS invalid_core_rows,
 COUNT(*) FILTER (WHERE customer_id IS NULL) AS missing_customer_ids,
 COUNT(*) FILTER (WHERE line_type = 'cancellation') AS cancellation_lines
FROM retail_clean;

-- 2. Monthly gross sales and cancellation adjustments; no cost data, so not profit.
SELECT DATE_TRUNC('month', invoice_date)::date AS month,
 ROUND(SUM(signed_line_value) FILTER (WHERE line_type='sale'),2) AS gross_sales,
 ROUND(ABS(COALESCE(SUM(signed_line_value) FILTER (WHERE line_type='cancellation'),0)),2) AS cancellation_adjustments,
 ROUND(COALESCE(SUM(signed_line_value) FILTER (WHERE line_type IN ('sale','cancellation')),0),2) AS net_signed_sales
FROM retail_clean WHERE invoice_date IS NOT NULL
GROUP BY 1 ORDER BY 1;

-- 3. Top products by gross sales (exclude canceled and invalid rows).
SELECT stock_code, MAX(description) AS product_description,
 SUM(quantity) AS units_sold, ROUND(SUM(signed_line_value),2) AS gross_sales
FROM retail_clean
WHERE line_type='sale' AND stock_code IS NOT NULL
GROUP BY stock_code ORDER BY gross_sales DESC LIMIT 15;

-- 4. Countries by gross sales.
SELECT country, COUNT(DISTINCT invoice_no) AS invoices,
 ROUND(SUM(signed_line_value),2) AS gross_sales
FROM retail_clean WHERE line_type='sale' AND country IS NOT NULL
GROUP BY country ORDER BY gross_sales DESC;

-- 5. Customer RFM-style features (recency, frequency, monetary), only known customer IDs.
WITH customer_stats AS (
 SELECT customer_id,
 MAX(invoice_date)::date AS last_purchase,
 COUNT(DISTINCT invoice_no) AS order_count,
 ROUND(SUM(signed_line_value),2) AS gross_spend
 FROM retail_clean WHERE line_type='sale' AND customer_id IS NOT NULL
 GROUP BY customer_id
)
SELECT customer_id, last_purchase,
 (SELECT MAX(invoice_date)::date FROM retail_clean) - last_purchase AS recency_days,
 order_count, gross_spend,
 NTILE(4) OVER (ORDER BY gross_spend DESC) AS spend_quartile
FROM customer_stats ORDER BY gross_spend DESC LIMIT 25;

-- 6. Cancellation overview; cancellation invoice values are not always directly matchable to sales.
SELECT DATE_TRUNC('month',invoice_date)::date AS month,
 COUNT(*) FILTER (WHERE line_type='cancellation') AS cancellation_lines,
 COUNT(*) FILTER (WHERE line_type='sale') AS sale_lines,
 ROUND(100.0 * COUNT(*) FILTER (WHERE line_type='cancellation') /
 NULLIF(COUNT(*) FILTER (WHERE line_type IN ('sale','cancellation')),0),2) AS cancellation_line_share_pct
FROM retail_clean WHERE invoice_date IS NOT NULL
GROUP BY 1 ORDER BY 1;
