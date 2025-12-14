import tkinter as tk
from tkinter import ttk
import threading
import requests
import websocket
import json
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches


class PriceVolumeChart:
    def __init__(self, parent, symbol):
        self.parent = parent
        self.symbol = symbol.lower()
        self.is_active = False
        self.ws = None

        self.times = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []

        self.frame = ttk.Frame(parent, style="Card.TFrame")

        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax_price = self.fig.add_subplot(211)
        self.ax_vol = self.fig.add_subplot(212, sharex=self.ax_price)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.fig.tight_layout()

    def start(self):
        if self.is_active:
            return
        self.is_active = True
        self.load_history()
        self.start_ws()

    def stop(self):
        self.is_active = False
        if self.ws:
            self.ws.close()
            self.ws = None

    def load_history(self):
        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": self.symbol.upper(),
            "interval": "1m",
            "limit": 60
        }

        def task():
            try:
                r = requests.get(url, params=params, timeout=5)
                klines = r.json()

                self.times.clear()
                self.opens.clear()
                self.highs.clear()
                self.lows.clear()
                self.closes.clear()
                self.volumes.clear()

                for k in klines:
                    self.times.append(datetime.fromtimestamp(k[0] / 1000).strftime("%H:%M"))
                    self.opens.append(float(k[1]))
                    self.highs.append(float(k[2]))
                    self.lows.append(float(k[3]))
                    self.closes.append(float(k[4]))
                    self.volumes.append(float(k[5]))

                self.parent.after(0, self.redraw)

            except Exception as e:
                print("REST error:", e)

        threading.Thread(target=task, daemon=True).start()

    def start_ws(self):
        url = f"wss://stream.binance.com:9443/ws/{self.symbol}@kline_1m"

        self.ws = websocket.WebSocketApp(
            url,
            on_message=self.on_ws_message,
            on_open=lambda ws: print(f"{self.symbol} kline connected"),
            on_close=lambda ws, a, b: print(f"{self.symbol} kline closed"),
            on_error=lambda ws, e: print(f"{self.symbol} kline error:", e)
        )

        threading.Thread(target=self.ws.run_forever, daemon=True).start()

    def on_ws_message(self, ws, message):
        if not self.is_active:
            return

        data = json.loads(message)
        k = data["k"]

        time = datetime.fromtimestamp(k["t"] / 1000).strftime("%H:%M")
        o = float(k["o"])
        h = float(k["h"])
        l = float(k["l"])
        c = float(k["c"])
        v = float(k["v"])
        closed = k["x"]

        self.parent.after(
            0,
            self.update_candle,
            time, o, h, l, c, v, closed
        )

    def update_candle(self, time, o, h, l, c, v, closed):
        if not self.opens:
            return

        if closed:
            self.times.append(time)
            self.opens.append(o)
            self.highs.append(h)
            self.lows.append(l)
            self.closes.append(c)
            self.volumes.append(v)
        else:
            self.highs[-1] = h
            self.lows[-1] = l
            self.closes[-1] = c
            self.volumes[-1] = v
            self.times[-1] = time

        self.times = self.times[-60:]
        self.opens = self.opens[-60:]
        self.highs = self.highs[-60:]
        self.lows = self.lows[-60:]
        self.closes = self.closes[-60:]
        self.volumes = self.volumes[-60:]

        self.redraw()

    def redraw(self):
        self.ax_price.clear()
        self.ax_vol.clear()

        width = 0.6
        volume_colors = []

        for i in range(len(self.opens)):
            o = self.opens[i]
            h = self.highs[i]
            l = self.lows[i]
            c = self.closes[i]

            color = "green" if c >= o else "red"
            volume_colors.append(color)

            # Wick
            self.ax_price.plot([i, i], [l, h], color=color, linewidth=1)

            # Body
            rect = patches.Rectangle(
                (i - width / 2, min(o, c)),
                width,
                max(abs(c - o), 0.0001),
                facecolor=color,
                edgecolor=color
            )
            self.ax_price.add_patch(rect)

        self.ax_price.axhline(self.closes[-1], linestyle="--", linewidth=1)
        self.ax_price.set_ylabel("Price")
        self.ax_price.grid(True)

        self.ax_price.xaxis.set_visible(False)

        self.ax_vol.bar(
            range(len(self.volumes)),
            self.volumes,
            color=volume_colors
        )

        self.ax_vol.set_ylabel("Volume")
        self.ax_vol.grid(True)

        step = 10
        self.ax_vol.set_xticks(range(0, len(self.times), step))
        self.ax_vol.set_xticklabels(self.times[::step], rotation=30)

        self.fig.tight_layout()
        self.canvas.draw()

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def pack_forget(self):
        self.frame.pack_forget()
