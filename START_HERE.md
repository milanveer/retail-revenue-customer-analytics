# End-to-end setup (Mac)

This project now supports **CSV/XLSX → Pandas → PostgreSQL → SQL cleaning view → Streamlit**. The existing direct-upload dashboard is still available. The dataset itself is not bundled.

## Prerequisites
- PostgreSQL running, with database `retail_analytics` created (already done in the tutorial).
- Python 3.10+ and a local copy of `Online Retail.xlsx` or its CSV export.
- The database login should match your Postgres.app local Mac user. If it does not, configure `DATABASE_URL` below.

## Run in VS Code terminal (project root)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python load_data.py "$HOME/Downloads/Online Retail.xlsx"
python run_pipeline.py
streamlit run app/dashboard.py
```
If your file is a CSV or has another name, change the quoted path accordingly. Use the **PostgreSQL (end-to-end pipeline)** radio option in the dashboard.

If your Postgres.app connection needs a username/password or non-default port, set `DATABASE_URL` before running scripts, e.g.:
```bash
export DATABASE_URL='postgresql+psycopg://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/retail_analytics'
```
Avoid committing passwords to GitHub. On Postgres.app, the default local setup often supports the URL used in the scripts without credentials.

## What each part does
- `load_data.py`: Pandas reads the real dataset, validates 8 fields, normalizes dates and text, and replaces the `retail_raw` staging table contents. All raw fields are text to avoid the earlier `C536379` invoice issue.
- `sql/02_cleaning.sql`: SQL view converts numeric and timestamp types, classifies sale vs cancellation vs other, and calculates signed line value.
- `run_pipeline.py`: Creates/replaces the view and prints row counts and KPIs for verification.
- `sql/03_analysis.sql`: Analyst SQL deliverables to run in DBeaver against the same PostgreSQL database.
- `app/dashboard.py`: Switch between original file-upload mode and a live PostgreSQL-backed mode.
- `docs/`: Business report and interview notes; fill in results only after validation.

## Data checks and limitations
Expected original file size is 541,909 rows. No dataset or actual SQL results are bundled. The dashboard calculates gross sales, not profit; the source lacks costs. Cancellation *lines* are not the same as cancellation *orders*. December 2011 is a partial month. This project is an independent case study, not employment experience.

If loading fails, paste the full terminal error; don't keep re-running an import blindly.
