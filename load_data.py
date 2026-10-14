"""Load the public UCI Online Retail CSV/XLSX into PostgreSQL raw staging."""
import argparse
import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

COLS = {'invoiceno':'invoice_no','stockcode':'stock_code','description':'description','quantity':'quantity','invoicedate':'invoice_date','unitprice':'unit_price','customerid':'customer_id','country':'country'}

def normalize(df):
    df.columns = [str(c).lower().replace('_','').strip() for c in df.columns]
    missing = set(COLS)-set(df.columns)
    if missing:
        raise ValueError(f'Missing dataset columns: {sorted(missing)}')
    df = df[list(COLS)].rename(columns=COLS)
    # Retain original invoice prefixes and preserve nulls. All raw database fields are text.
    for col in df.columns:
        if col == 'invoice_date':
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
        elif col in ('quantity','unit_price'):
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('string')
        else:
            df[col] = df[col].astype('string').str.strip()
    df['customer_id'] = df['customer_id'].str.replace(r'\.0$', '', regex=True)
    return df.astype(object).where(pd.notna(df), None)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('file', type=Path, help='Original Online Retail.xlsx or CSV')
    parser.add_argument('--database-url', default=os.getenv('DATABASE_URL', 'postgresql+psycopg://localhost:5432/retail_analytics'))
    args=parser.parse_args()
    if not args.file.exists():
        parser.error(f'File not found: {args.file}')
    engine=create_engine(args.database_url)
    with engine.begin() as conn:
        conn.execute(text('''CREATE TABLE IF NOT EXISTS retail_raw (
            invoice_no TEXT, stock_code TEXT, description TEXT, quantity TEXT,
            invoice_date TEXT, unit_price TEXT, customer_id TEXT, country TEXT)'''))
        # Clear only after a successful source-file read (prevents duplicate loads).
    if args.file.suffix.lower()=='.xlsx':
        batches=[pd.read_excel(args.file, engine='openpyxl')]
    else:
        batches=pd.read_csv(args.file, chunksize=25000, encoding='utf-8-sig', low_memory=False, dtype=str)
    count=0
    with engine.begin() as conn:
        conn.execute(text('TRUNCATE TABLE retail_raw'))
        for batch in batches:
            clean=normalize(batch)
            clean.to_sql('retail_raw', conn, if_exists='append', index=False, chunksize=1000, method='multi')
            count+=len(clean)
            print(f'Loaded {count:,} rows')
    with engine.connect() as conn:
        actual=conn.execute(text('SELECT COUNT(*) FROM retail_raw')).scalar_one()
    print(f'Complete: {actual:,} raw rows in PostgreSQL')
    if actual!=541909:
        print('NOTE: Original UCI dataset has 541,909 rows. Confirm you used the complete file.')

if __name__=='__main__':
    main()
