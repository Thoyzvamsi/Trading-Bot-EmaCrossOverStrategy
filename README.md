# EMA Crossover Trading Bot (Python)

A modular rule-based trading bot built using Python and SmartAPI that automates market data collection, signal generation, and trade execution using an EMA crossover strategy.

The project was designed to simulate a structured trading pipeline instead of relying on unorganized scripts. It separates data collection, preprocessing, strategy logic, and execution into independent modules for easier testing and future scalability.

---

## 🚀 Overview

This trading system follows a complete pipeline:

- Fetches live and historical market data using SmartAPI
- Preprocesses and structures raw market data
- Calculates EMA-based indicators
- Generates buy/sell signals
- Executes trades automatically
- Stores trade logs for tracking performance

The strategy currently focuses on trend-following momentum using a dual EMA crossover model on 15-minute candles.

---

## 🧠 Current Strategy Structure

The bot uses a **dual EMA crossover strategy**:

- **EMA 14** → Short-term trend direction
- **EMA 50** → Long-term trend direction

### Entry Logic
- Buy when EMA 14 crosses above EMA 50  
  *(Golden Cross)*

### Exit Logic
- Sell when EMA 14 crosses below EMA 50  
  *(Death Cross)*

The strategy continuously checks for the latest candle data every 60 seconds and updates signals dynamically.

---

## 📁 Project Structure

```bash
TRADING-BOT/
│
├── data/
│   └── normal_data/
│       ├── raw_data.csv        # Raw historical market data
│       └── prep_data.csv       # Processed data with indicators/signals
│
├── data_pipeline/
│   ├── data_prep.py            # Data preprocessing & feature generation
│   └── strategy.py             # Trading strategy and execution logic
│
├── logs/                       # Runtime logs
│
├── src/
│   └── source.py               # SmartAPI session & market data handling
│
├── main.py                     # Main execution file
│
└── README.md
```

---

## ⚙️ How To Use

### Setup

- Clone the repository
- Install required dependencies
- Add your SmartAPI credentials inside `main.py`
- Add the stock symbol and token you want to trade

Example:

```
symbol = "SBIN-EQ"
symbol_token = "3045"
credentials = [
    "API_KEY",
    "CLIENT_ID",
    "PASSWORD",
    "TOTP_SECRET"
]
```

Run the bot using:
```bash
python main.py
```

For continuous execution during market hours, the bot can be deployed on a VPS server.

---
## 🔄 Trading System Workflow

        SmartAPI
            │
            ▼
   Market Data Collection
        (source.py)
            │
            ▼
     Raw Data Storage
      raw_data.csv
            │
            ▼
    Data Preprocessing
      (data_prep.py)
            │
            ▼
   EMA Indicator Creation
      EMA 14 & EMA 50
            │
            ▼
     Signal Generation
   Buy / Sell Conditions
            │
            ▼
    Strategy Execution
      (strategy.py)
            │
            ▼
      Order Placement
        BUY / SELL
            │
            ▼
       Trade Logging
      trade_data.json

---

## 🚧 Future Enhancements

- Add custom strategies inside `strategy.py`
- Add feature engineering and indicators inside `data_prep.py`
- Implement Stop Loss and Risk Management
- Add Streamlit dashboard for live monitoring
- Add Telegram or Email trade alerts
- Support multiple stocks simultaneously

---

## ⚠️ Disclaimer

This project is built for educational and research purposes only.  
It should not be considered financial advice or a guarantee of profitability.