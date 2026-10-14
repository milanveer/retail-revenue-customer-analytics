# Business findings report — complete after running the real data

## Executive question
Which products, customers, countries, and months contribute most to gross sales, and how significant are cancellation line items?

## Method
Public UCI Online Retail transaction-level data; typed raw columns, flagged canceled invoices, computed line-level gross sales, aggregated by month/product/country/customer.

## Verified results (fill from SQL/dashboard)
- Imported rows: [VERIFY]
- Date range: [VERIFY]
- Gross sales: [VERIFY]
- Leading products by sales: [VERIFY]
- Leading markets by sales: [VERIFY]
- Cancellation lines / share: [VERIFY]
- Missing customer IDs: [VERIFY]

## Recommendations (conditional until validated)
1. Review top-revenue products for inventory availability, *if* concentration is high.
2. Investigate high-cancellation product or time segments, *if* such patterns emerge.
3. Prioritize high-value repeat customers for retention experiments, *if* customer-level data is sufficiently complete.

## Important caveats
No product costs: do not claim profit or margin insights. Negative quantities and canceled invoice IDs are proxies for reversals; do not claim they all represent refunded orders. Observational data cannot establish causality.

## Stakeholder deliverable
Present 3 charts, 3 verified insights, 2 recommendations, 1 data limitation, and the next business question to investigate.
