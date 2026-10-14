# Retail Revenue & Customer Analytics

**Independent DA/BA portfolio case study** using real historical transaction data from the UCI Online Retail dataset (UK online retailer, 2010–2011). This is **not employment experience**.

## Business brief
Leadership wants to understand monthly sales, strongest products/markets, customer concentration, and cancellation patterns. Recommendations must be supported by actual results. The data does not contain product cost, so **profitability cannot be inferred**.

## Data source
UCI Machine Learning Repository: https://archive.ics.uci.edu/dataset/352/online+retail (541,909 line-item rows in original dataset). Download `Online Retail.xlsx` yourself; it is not redistributed in this repository.

## Quick-start dashboard (Mac)
```bash
cd retail_analytics_portfolio
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/dashboard.py
```
Upload your `Online Retail.xlsx` or exported CSV in the browser. Charts and metrics are calculated from the file; none are hardcoded.

## PostgreSQL workflow
1. Create/connect to the `retail_analytics` database.
2. Run `sql/01_schema.sql` to create `retail_raw` with **all text columns**. This prevents DBeaver's `C536379` invoice parse error.
3. In DBeaver, import CSV to `retail_raw` and explicitly map the 8 source fields to the 8 target fields; do **not** create new columns. Keep the header setting enabled. If the CSV has dates in another format, adjust `02_cleaning.sql`.
4. Verify `SELECT COUNT(*) FROM retail_raw;` returns 541909 for the complete original file.
5. Run `sql/02_cleaning.sql`, then `sql/03_analysis.sql`.

The SQL and dashboard are two complementary implementations. The dashboard reads the uploaded file directly; PostgreSQL is used for analyst SQL deliverables.

## KPI definitions
- **Gross sales**: positive quantity × positive unit price on non-cancellation lines.
- **Cancellation line count**: line items with `C`-prefixed invoice or negative quantity. This is **not** a cancellation rate by order.
- **Net signed sales**: sum of signed line values on sales and cancellation lines; not accounting net revenue.
- **Customer count**: unique non-null customer IDs on sales lines.
- **Recency**: days since last purchase relative to latest date in dataset.

## Limitations
Historical single-company data; unknown currency conversions; missing customer IDs; returns/cancellations cannot always be matched to original sales; no costs, margins, acquisition channels, or shipping data. Do not claim causal effects.

## Deliverables
- `sql/`: raw staging schema, cleaning view, six analytical queries
- `app/dashboard.py`: interactive dashboard with country filters and data-quality checks
- `docs/`: business presentation template and interview walkthrough

## Next steps
Run with the actual downloaded file, record query outputs and dashboard screenshots, then replace placeholders in the business report with verified results. Publish to GitHub only after you understand and can reproduce the analysis.
