# Real-Time Crypto Dashboard

A **real-time crypto dashboard** built with Python and Tkinter that displays live **chart, ticker, trade data, and order book** for multiple coins using Binance WebSocket API.

---

## Project (preliminary) UI design

https://www.figma.com/design/OgDHCNLW9d6Go8hVhKocY4/Untitled?node-id=0-1&t=LeGWAxQciRqKX82n-1

---

## Demonstrate Video

https://youtu.be/97yS452wUQs

---

## Features

- **Price & Volume Chart:** Displays live candlestick chart and volume.
- **Live Ticker:** Shows current price and volume (24H) updates for selected coins.
- **Market Trades:** Tracks real-time trades.
- **Order Book:** Shows live bid/ask orders in real-time.
- **Multiple Coins:** Supports BTC, ETH, SOL, LINK, XRP, DOGE.
- **Coin Selection:** Easily switch between coins using a dropdown.
- **Show/Hide Info:** Toggle the ticker and order book visibility.
- **Persistent Preferences:** Saves the last selected coin and hide/show state.

---

## Project Structure

```
crypto_dashboard/
│
├─ main.py                 # Entry point of the application
├─ components/
│   ├─ ticker.py           # CryptoTicker class
│   ├─ order_book.py       # OrderBook class
│   └─ chart.py            # PriceVolumeChart class
├─ utils/
│   ├─ preferences.py      # Save/load user preferences
│   └─ preferences.json    # Place where preferences are saved
├─ README.md               # This file
└─ requirements.txt        # Requirements to run this project
```

---

## How to run

Run these commands in terminal.

```bash
git clone https://github.com/LELOUCH2L/crypto_dashboard
cd crypto_dashboard
pip install -r requirements.txt
python main.py
```
