import tkinter as tk
from tkinter import ttk
import websocket
import json
import threading


class OrderBook:
    def __init__(self, parent_1, parent_2,symbol):
        self.parent_1 = parent_1
        self.parent_2 = parent_2
        self.symbol = symbol.lower()
        self.is_active = False
        self.order_ws = None

        # Ask
        self.ask_frame = ttk.Frame(self.parent_1, style="Order.TFrame")

        self.ask_list = tk.Listbox(
            self.ask_frame,
            height=12,
            bg="#1A1D20",
            fg="#F6465D",
            font=("Consolas", 10),
            activestyle='none',
            highlightthickness=0,
            bd=0
        )
        self.ask_list.pack(fill=tk.BOTH, expand=True)

        # Bid
        self.bid_frame = ttk.Frame(self.parent_2, style="Order.TFrame")

        self.bid_list = tk.Listbox(
            self.bid_frame,
            height=12,
            bg="#1A1D20",
            fg="#0ECB81",
            font=("Consolas", 10),
            activestyle='none',
            highlightthickness=0,
            bd=0
        )
        self.bid_list.pack(fill=tk.BOTH, expand=True)

    def start(self):
        if self.is_active:
            return

        self.is_active = True

        order_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@depth20@100ms"

        self.order_ws = websocket.WebSocketApp(
            order_url,
            on_message=self.on_order_book,
            on_error=lambda ws, error: print(f"{self.symbol} order error: {error}"),
            on_close=lambda ws, status, message: print(f"{self.symbol} order closed"),
            on_open=lambda ws: print(f"{self.symbol} order connected")
        )

        threading.Thread(target=self.order_ws.run_forever, daemon=True).start()

    def stop(self):
        self.is_active = False
        if self.order_ws:
            self.order_ws.close()
            self.order_ws = None

    def on_order_book(self, ws, message):
        if not self.is_active:
            return

        data = json.loads(message)
        asks = data["asks"]
        bids = data["bids"]

        self.parent_1.after(0, self.update_order_book, asks, bids)
        self.parent_2.after(0, self.update_order_book, asks, bids)

    def update_order_book(self, asks, bids):
        self.ask_list.delete(0, tk.END)
        self.bid_list.delete(0, tk.END)

        for price, amount in reversed(asks):
            self.ask_list.insert(tk.END, f" {float(price):<11,.2f} {float(amount):.4f}")

        for price, amount in bids:
            self.bid_list.insert(tk.END, f" {float(price):<11,.2f} {float(amount):.4f}")

    def pack(self, **kwargs):
        self.ask_frame.pack(**kwargs)
        self.bid_frame.pack(**kwargs)

    def pack_forget(self):
        self.ask_frame.pack_forget()
        self.bid_frame.pack_forget()
