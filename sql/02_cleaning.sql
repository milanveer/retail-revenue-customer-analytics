-- A reusable cleaned view; retains cancellations and separates them from sales.
CREATE OR REPLACE VIEW retail_clean AS
WITH typed AS (
 SELECT NULLIF(TRIM(invoice_no),'') AS invoice_no,
        NULLIF(TRIM(stock_code),'') AS stock_code,
        NULLIF(TRIM(description),'') AS description,
        CASE WHEN TRIM(quantity) ~ '^-?[0-9]+$' THEN TRIM(quantity)::INTEGER END AS quantity,
        CASE WHEN TRIM(unit_price) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN TRIM(unit_price)::NUMERIC END AS unit_price,
        NULLIF(TRIM(customer_id),'') AS customer_id,
        NULLIF(TRIM(country),'') AS country,
        CASE WHEN TRIM(invoice_date) ~ '^\d{1,2}/\d{1,2}/\d{4} ' THEN to_timestamp(TRIM(invoice_date),'MM/DD/YYYY HH24:MI')::timestamp
             WHEN TRIM(invoice_date) ~ '^\d{4}-\d{2}-\d{2} ' THEN TRIM(invoice_date)::timestamp END AS invoice_date
 FROM retail_raw
)
SELECT *, CASE WHEN invoice_no LIKE 'C%' OR quantity < 0 THEN 'cancellation'
               WHEN quantity > 0 AND unit_price > 0 THEN 'sale'
               ELSE 'other' END AS line_type,
       quantity * unit_price AS signed_line_value
FROM typed;
