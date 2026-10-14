"""Streamlit dashboard for the public UCI Online Retail dataset."""
import io
import pandas as pd
import os
from sqlalchemy import create_engine, text
import streamlit as st

st.set_page_config(page_title='Retail Revenue Analytics', layout='wide')
st.title('Retail Revenue & Customer Analytics')
st.caption('Independent case study · UCI Online Retail (2010–2011) · Revenue, not profit')

@st.cache_data(show_spinner=False)
def load_bytes(data: bytes, filename: str):
    if filename.lower().endswith('.xlsx'):
        return pd.read_excel(io.BytesIO(data), engine='openpyxl')
    return pd.read_csv(io.BytesIO(data), encoding='utf-8-sig', low_memory=False)

source=st.radio('Data source', ['Upload CSV / Excel', 'PostgreSQL (end-to-end pipeline)'], horizontal=True)
if source == 'PostgreSQL (end-to-end pipeline)':
    try:
        engine=create_engine(os.getenv('DATABASE_URL', 'postgresql+psycopg://localhost:5432/retail_analytics'))
        query="""SELECT invoice_no AS invoiceno, stock_code AS stockcode,
            description, quantity, invoice_date AS invoicedate, unit_price AS unitprice,
            customer_id AS customerid, country, line_type,
            signed_line_value AS line_value FROM retail_clean"""
        with engine.connect() as conn:
            df=pd.read_sql(text(query), conn)
        st.success(f'Connected to PostgreSQL: {len(df):,} records from retail_clean')
    except Exception as exc:
        st.error(f'Could not read PostgreSQL: {exc}')
        st.info('Run python load_data.py <path-to-file> and python run_pipeline.py first.')
        st.stop()
else:
    uploaded = st.file_uploader('Upload the original Online Retail.xlsx or online_retail.csv', type=['xlsx','csv'])
    if uploaded is None:
        st.info('Upload the public dataset to populate this dashboard with verified results. No results are fabricated.')
        st.stop()

    raw = load_bytes(uploaded.getvalue(), uploaded.name)
    raw.columns = [str(c).lower().replace('_','').strip() for c in raw.columns]
    required = {'invoiceno','stockcode','description','quantity','invoicedate','unitprice','customerid','country'}
    if not required.issubset(raw.columns):
        st.error(f'Missing expected columns: {sorted(required-set(raw.columns))}')
        st.stop()
    df = raw.copy()
    df['quantity'] = pd.to_numeric(df['quantity'],errors='coerce')
    df['unitprice'] = pd.to_numeric(df['unitprice'],errors='coerce')
    df['invoicedate'] = pd.to_datetime(df['invoicedate'],errors='coerce')
    df['invoiceno'] = df['invoiceno'].astype('string').str.strip()
    df['country'] = df['country'].astype('string').str.strip()
    df['customerid'] = df['customerid'].astype('string').str.replace(r'\.0$', '', regex=True)
    df['line_type'] = 'other'
    df.loc[(df.quantity > 0) & (df.unitprice > 0),'line_type']='sale'
    df.loc[df.invoiceno.str.startswith('C',na=False) | (df.quantity < 0),'line_type']='cancellation'
    df['line_value'] = df.quantity * df.unitprice


# Normalize file and database representations.
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
df['unitprice'] = pd.to_numeric(df['unitprice'], errors='coerce')
df['line_value'] = pd.to_numeric(df['line_value'], errors='coerce')
df['invoicedate'] = pd.to_datetime(df['invoicedate'], errors='coerce')
df['country'] = df['country'].astype('string').str.strip()
df['customerid'] = df['customerid'].astype('string').str.replace(r'\.0$', '', regex=True)
st.sidebar.header('Filters')
countries = sorted(df.country.dropna().unique().tolist())
selected = st.sidebar.multiselect('Country', countries, default=countries)
view = df[df.country.isin(selected)]
sales = view[view.line_type.eq('sale') & view.invoicedate.notna()]
cancel = view[view.line_type.eq('cancellation')]

c1,c2,c3,c4=st.columns(4)
c1.metric('Gross sales',f'£{sales.line_value.sum():,.0f}')
c2.metric('Sales invoices',f'{sales.invoiceno.nunique():,}')
c3.metric('Cancellation lines',f'{len(cancel):,}')
c4.metric('Customers (known IDs)',f'{sales.customerid.dropna().nunique():,}')

st.subheader('Monthly gross sales')
monthly = sales.groupby(sales.invoicedate.dt.to_period('M')).line_value.sum()
monthly.index = monthly.index.astype(str)
st.line_chart(monthly)

left,right=st.columns(2)
with left:
    st.subheader('Top 10 products by gross sales')
    products=sales.groupby(['stockcode','description'],dropna=False).line_value.sum().sort_values(ascending=False).head(10)
    st.bar_chart(products.reset_index().set_index('description').line_value)
with right:
    st.subheader('Top 10 countries by gross sales')
    st.bar_chart(sales.groupby('country').line_value.sum().nlargest(10))

st.subheader('Data quality')
st.write({'raw_rows':len(df),'missing_customer_ids':int(df.customerid.isna().sum()),
          'missing_dates':int(df.invoicedate.isna().sum()),'cancellation_lines':len(cancel),
          'other_lines':int(df.line_type.eq('other').sum())})
st.caption('Cancellations are identified by C-prefixed invoices or negative quantities. Gross sales exclude cancellation lines. Product costs are unavailable, so profitability cannot be measured.')
