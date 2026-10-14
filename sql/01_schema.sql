-- Run inside the retail_analytics database. Raw text staging avoids CSV type-inference errors.
CREATE TABLE IF NOT EXISTS retail_raw (
  invoice_no TEXT, stock_code TEXT, description TEXT, quantity TEXT,
  invoice_date TEXT, unit_price TEXT, customer_id TEXT, country TEXT
);
-- After importing the CSV into retail_raw, run 02_cleaning.sql.
