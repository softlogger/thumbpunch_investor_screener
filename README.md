# ThumbPunch Investor Screener

ThumbPunch Investor Screener is a transparent, multi-source stock-screening application.

The initial version will:

- Accept a single stock ticker
- Retrieve financial data from multiple providers
- Normalize comparable financial fields
- Highlight material discrepancies between providers
- Allow the user to select a primary data provider
- Apply Joe_Investor's five screening criteria
- Show PASS, FAIL, or DATA UNAVAILABLE for each criterion
- Explain why the stock qualified or did not qualify

The first development providers are:

- Financial Modeling Prep (FMP)
- Yahoo Finance

Fiscal.ai will be added when API access becomes available.

The application will initially be developed locally, then deployed to Microsoft Azure and connected to:

https://www.thumbPunch.com