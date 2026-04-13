# Financial Market Data Extractor (yFinance Bot)
This repository contains a Python-based automation tool designed to fetch real-time financial market data using the Yahoo Finance API. It automates the extraction of historical prices, tickers, and key financial metrics for further analysis or reporting.

# 📌 Problem & Solution
Manually tracking market data for multiple tickers is inefficient and limits the ability to perform high-frequency or large-scale analysis. Relying on manual downloads leads to outdated information and slowed decision-making.

This automation bot:

Eliminates manual data fetching by automating the API connection to Yahoo Finance.

Streamlines ticker monitoring by processing multiple financial instruments simultaneously.

Formats raw market data into clean, analysis-ready structures (DataFrames/CSV).

Provides reliable execution tracking through integrated logging.

# 🛠 Tech Stack
**Python:** Core programming for API orchestration and automation.

**yFinance:** Primary library for financial data extraction.

**Pandas:** Data structuring and export management.

**Logging:** To monitor API requests and handle connection status.

# ⚙️ Core Automation Workflow
**Request:** Initializes an automated connection to the yFinance API for a specified list of tickers.

**Extraction:** Fetches historical price data, volume, and company metadata.

**Data Processing:** Cleans and structures the raw API response using Pandas.

**Storage/Export:** Saves the structured financial data as CSV or prepares it for downstream analytics.

# 📊 Example Output
When the script is executed, it provides a summary of the extracted market data and database status:

```
INFO:root:Stock data successfully written to the database.
INFO:root:Total rows inserted: 33
INFO:root:Amazon Summary: {'Last Close': 232.52, 'Daily Change': 0.45, 'Mean Close': 228.23, ...}
INFO:root:Apple Summary: {'Last Close': 272.82, 'Daily Change': -0.67, 'Mean Close': 272.81, ...}
INFO:root:Tesla Summary: {'Last Close': 454.42, 'Daily Change': -5.21, 'Mean Close': 476.90, ...}
```

# 🚀 How to Run
1. Ensure you have the ticker list ready in the configuration.

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the automation:

```
python "yfinance bot/src/stock-market-data-bot.py"
```

