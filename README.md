# EMA Crossover Trading Bot (Python)

A rule-based trading bot that generates buy/sell signals using a dual EMA crossover strategy and evaluates performance through backtesting.

---

## 🚀 Overview

This project implements a structured trading pipeline:

- Market data collection (SmartAPI)
- Indicator calculation (EMA 14 & EMA 50)
- Signal generation

The goal was to build a clean and testable trading system instead of unstructured scripts.

---

## 🧠 Strategy Logic

This bot uses a **trend-following EMA crossover strategy**.

**Indicators Used:**
- EMA 14 (short-term trend)
- EMA 50 (long-term trend)

**Entry Conditions:**
- Buy when EMA 14 crosses above EMA 50 (Golden Cross)

**Exit Conditions:**
- Sell when EMA 14 crosses below EMA 50 (Death Cross)

---

## 📊 Backtest Results

- Back tested this strategy before Building A trading Bot

**Stock:** Canara Bank  
**Period:** 5 Years  
**Total Trades:** 469  

| Metric            | Value |
|------------------|------|
| Win Rate         | 29.27% |
| Avg Win          | ₹402.05 |
| Avg Loss         | ₹-120.85 |
| Max Drawdown     | -21.24% |
| Profit Factor    | 1.38 |
| Sharpe Ratio     | 0.55 |
| Total Returns    | ₹15,027 |

---

### 🧠 Interpretation

- Low win rate (~29%) but profitable due to **higher average wins vs losses**
- Profit Factor > 1 → Strategy is profitable
- Drawdown (~21%) is moderate → risk needs improvement
- Sharpe Ratio is low → returns are not very efficient

