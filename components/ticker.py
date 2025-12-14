import tkinter as tk
from tkinter import ttk
import websocket
import json
import threading
from datetime import datetime


class CryptoTicker:
    def __init__(self, parent, symbol):
        self.parent = parent
        self.symbol = symbol.lower()
        self.is_active = False
        self.ticker_ws = None
        self.trade_ws = None

        self.left_frame = ttk.Frame(parent, style="TFrame")
        self.right_frame = ttk.Frame(parent, style="TFrame")

        # Price
        self.price_frame = ttk.Frame(self.left_frame, padding=10, style="Card.TFrame")
        self.price_frame.pack(fill=tk.BOTH, expand=True, padx=(0, 20), pady=(0, 20))

        self.price_title_label = ttk.Label(self.price_frame, text="Price", font=("Bahnschrift", 12, "bold"), anchor=tk.W, style="Card.TLabel").pack(fill=tk.X)

        self.price_label = ttk.Label(self.price_frame, text="--", font=("Consolas", 12, "bold"), anchor=tk.W, style="Card.TLabel")
        self.price_label.pack(fill=tk.X, pady=(10,5))

        self.change_label = ttk.Label(self.price_frame, text="--", font=("Consolas", 10, "bold"), anchor=tk.W, style="Card.TLabel")
        self.change_label.pack(fill=tk.X)

        # Volume
        self.volume_frame = ttk.Frame(self.left_frame, padding=10, style="Card.TFrame")
        self.volume_frame.pack(fill=tk.BOTH, expand=True, padx=(0, 20))

        self.volume_title_label = ttk.Label(self.volume_frame, text="Volume", font=("Bahnschrift", 12, "bold"), anchor=tk.W, style="Card.TLabel").pack(fill=tk.X)

        self.volume_label = ttk.Label(self.volume_frame, text="--", font=("Consolas", 12, "bold"), anchor=tk.W, style="Card.TLabel")
        self.volume_label.pack(fill=tk.X, pady=(10, 0))

        # Market Trades
        self.market_trades_frame = ttk.Frame(self.right_frame, padding=10, style="Card.TFrame")
        self.market_trades_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.market_trades_label = ttk.Label(self.market_trades_frame, text="Market Trades", font=("Bahnschrift", 12, "bold"), anchor=tk.W, style="Card.TLabel").pack(fill=tk.X, pady=(0, 10))

        self.market_trades_categories_label = ttk.Label(self.market_trades_frame, text=f" {"Time":<12} {"Side":<12} {"Price":<13} {"Amount":<14} Total", font=("Consolas", 10, "bold"), anchor=tk.W, style="Card.TLabel").pack(fill=tk.X)

        self.trade_list = tk.Listbox(
            self.market_trades_frame,
            height=8,
            bg="#1A1D20",
            fg="white",
            font=("Consolas", 10),
            activestyle='none',
            highlightthickness=0,
            bd=0
        )
        self.trade_list.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

    def start(self):
        if self.is_active:
            return

        self.is_active = True

        ticker_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@ticker"

        self.ticker_ws = websocket.WebSocketApp(
            ticker_url,
            on_message=self.on_message,
            on_error=lambda ws, error: print(f"{self.symbol} ticker error: {error}"),
            on_close=lambda ws, status, message: print(f"{self.symbol} ticker closed"),
            on_open=lambda ws: print(f"{self.symbol} ticker connected")
        )

        threading.Thread(target=self.ticker_ws.run_forever, daemon=True).start()

        trade_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@trade"

        self.trade_ws = websocket.WebSocketApp(
            trade_url,
            on_message=self.on_trade_message,
            on_error=lambda ws, error: print(f"{self.symbol} trade error: {error}"),
            on_close=lambda ws, status, message: print(f"{self.symbol} trade closed"),
            on_open=lambda ws: print(f"{self.symbol} trade connected")
        )

        threading.Thread(target=self.trade_ws.run_forever, daemon=True).start()

    def stop(self):
        self.is_active = False
        if self.ticker_ws:
            self.ticker_ws.close()
            self.ticker_ws = None
        if self.trade_ws:
            self.trade_ws.close()
            self.trade_ws = None

    def on_message(self, ws, message):
        if not self.is_active:
            return

        data = json.loads(message)
        price = float(data['c'])
        change = float(data['p'])
        percent = float(data['P'])
        volume = float(data['v'])

        self.parent.after(0, self.update_display, price, change, percent, volume)

    def update_display(self, price, change, percent, volume):
        if not self.is_active:
            return

        color = "#0ECB81" if change >= 0 else "#F6465D"
        self.price_label.config(text=f"{price:,.2f}", foreground=color)

        sign = "+" if change >= 0 else ""
        self.change_label.config(text=f"{sign}{change:,.2f} ({sign}{percent:.2f}%)",foreground=color)

        self.volume_label.config(text=f"{volume:,.2f}")

    def on_trade_message(self, ws, message):
        if not self.is_active:
            return

        data = json.loads(message)
        price = float(data["p"])
        amount = float(data["q"])
        is_sell = data["m"]
        side = "ASK" if is_sell else "BID"

        self.parent.after(0, self.add_trade_to_list, price, amount, is_sell, side)

    def add_trade_to_list(self, price, amount, is_sell, side):
        time = datetime.now().strftime("%H:%M:%S")
        text = f" {time:<12} {side:<12} {price:<13,.2f} {amount:<14,.4f} {(price * amount):,.2f}"

        self.trade_list.insert(0, text)
        self.trade_list.itemconfig(0, fg="#F6465D" if is_sell else "#0ECB81")

        if self.trade_list.size() > 8:
            self.trade_list.delete(8)

    def pack(self, **kwargs):
        self.left_frame.pack(**kwargs)
        self.right_frame.pack(**kwargs)

    def pack_forget(self):
        self.left_frame.pack_forget()
        self.right_frame.pack_forget()
