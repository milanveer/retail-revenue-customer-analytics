"""Build cleaned SQL view and print validation metrics."""
import os
from pathlib import Path
from sqlalchemy import create_engine, text

root=Path(__file__).resolve().parent
engine=create_engine(os.getenv('DATABASE_URL','postgresql+psycopg://localhost:5432/retail_analytics'))
with engine.begin() as conn:
    conn.execute(text((root/'sql/02_cleaning.sql').read_text()))
    for label, query in {
        'Raw rows':'SELECT COUNT(*) FROM retail_raw',
        'Clean view rows':'SELECT COUNT(*) FROM retail_clean',
        'Sales lines':"SELECT COUNT(*) FROM retail_clean WHERE line_type='sale' AND invoice_date IS NOT NULL",
        'Cancellation lines':"SELECT COUNT(*) FROM retail_clean WHERE line_type='cancellation'",
        'Gross sales':"SELECT ROUND(SUM(signed_line_value),2) FROM retail_clean WHERE line_type='sale' AND invoice_date IS NOT NULL",
    }.items():
        print(f'{label}: {conn.execute(text(query)).scalar_one()}')
print('SQL cleaning view ready. Launch: streamlit run app/dashboard.py')
