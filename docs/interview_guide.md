# Interview walkthrough — practice, don't memorize

## 30-second project summary
"I built an independent retail analytics case study using a public dataset of over 540,000 transaction line items. I used PostgreSQL to structure and query the data, including handling cancellations and missing customer IDs. I built an interactive dashboard to explore sales trends, products, and markets. I focused on distinguishing revenue from profit because product costs were not available."

Only say **I built** for parts you can personally explain and reproduce. If using assistance, say so truthfully when asked.

## Explain the pipeline
CSV / Excel → text-based PostgreSQL staging table → typed/cleaned SQL view → KPI and segmentation queries → interactive Streamlit dashboard (dashboard separately reads uploaded source file).

## Why stage as text?
An invoice number such as `C536379` is an identifier, not a numeric value. Importing all source columns as text prevents schema inference failures and lets us validate types deliberately.

## Common questions and answer points
1. **Why exclude cancellations from gross sales?** Gross sales measures positive sales lines; cancellation adjustments are reported separately.
2. **Why not call this profitability analysis?** The dataset lacks costs and margins.
3. **How did you handle missing customer IDs?** Include those rows in aggregate sales, but exclude unknown IDs from customer-level segmentation.
4. **How would you validate an import?** Row counts, null checks, date ranges, data-type checks, outliers, duplicate investigation, reconciliation of aggregates.
5. **Why use SQL?** Repeatable transformations, grouping, joins where needed, and transparent business definitions.
6. **How would you communicate findings?** State a quantified result, business implication, caveat, and action with a testable success metric.
7. **How does this relate to BA work?** Translate stakeholder questions into KPI definitions, scope, acceptance criteria, and actionable recommendations.

## Mock interviewer prompts
- Explain your biggest data-quality problem and how you diagnosed it.
- Walk through the monthly sales query line by line.
- What is the difference between invoice-level cancellation rate and line-level cancellation share?
- How would you identify repeat customers without double-counting line items?
- What data would you request to calculate profit margins?

## Resume bullet (after fully reproducing)
"Developed a PostgreSQL-based retail transaction analysis and interactive dashboard using a public 541K-row dataset; defined sales and cancellation KPIs, analyzed product/market trends, and documented data-quality limitations."
