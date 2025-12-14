import tkinter as tk
from tkinter import ttk
from components.ticker import CryptoTicker
from components.order_book import OrderBook
from components.chart import PriceVolumeChart
from utils import preferences

class TickerApp:
    BG = "#0B0E11"
    CARD_BG = "#1A1D20"
    TEXT_MAIN = "#EAECEF"
    ORDER_BOX = "#1A1D20"

    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Binance Dashboard")
        self.root.geometry("1000x762")
        root.configure(bg=self.BG)

        style = ttk.Style()
        style.configure("TFrame", background=self.BG)
        style.configure("Card.TFrame", background=self.CARD_BG)
        style.configure("TLabel", background=self.BG, foreground=self.TEXT_MAIN)
        style.configure("Card.TLabel", background=self.CARD_BG, foreground=self.TEXT_MAIN)
        style.configure("Order.TFrame", background=self.ORDER_BOX)

        # Top frame
        self.top_frame = ttk.Frame(self.root, style="TFrame")
        self.top_frame.pack(fill=tk.X, padx=20, pady=(20, 0))

        self.title_label = ttk.Label(self.top_frame, text="BTC/USDT DASHBOARD", font=("Bahnschrift", 22, "bold"))
        self.title_label.pack(side=tk.LEFT, anchor=tk.W, padx=(0, 10))

        self.choice = tk.StringVar()
        self.combo = ttk.Combobox(
            self.top_frame,
            textvariable=self.choice,
            values=["BTC/USDT", "ETH/USDT", "SOL/USDT", "LINK/USDT", "XRP/USDT", "DOGE/USDT"],
            state="readonly",
            width=11
        )
        self.combo.pack(side=tk.LEFT, pady=(5, 0))
        self.combo.bind("<<ComboboxSelected>>", self.on_coin_change)

        self.is_hidden = preferences.load_preference("is_hidden_info", False)
        self.show_hide_btn = ttk.Button(
            self.top_frame,
            text="Show Info" if self.is_hidden else "Hide Info",
            command=self.toggle_show_hide
        )
        self.show_hide_btn.pack(side=tk.RIGHT)

        # Main frame
        self.main_frame = ttk.Frame(self.root, style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.left_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(20, 0))
        self.right_frame.config(width=200)
        self.right_frame.pack_propagate(False)

        # Chart frame
        self.chart_frame = ttk.Frame(self.left_frame, style="Card.TFrame")
        self.chart_frame.pack(fill=tk.BOTH, expand=True)

        # Order book frame
        self.order_title = ttk.Label(
            self.right_frame,
            text="Order Book",
            font=("Bahnschrift", 12, "bold"),
            anchor=tk.W,
            background=self.CARD_BG,
            foreground=self.TEXT_MAIN
        )
        self.order_title.pack(fill=tk.X, padx=10, pady=10)

        self.header_frame = ttk.Frame(self.right_frame, style="Card.TFrame")
        self.header_frame.pack(fill=tk.X, padx=10)
        ttk.Label(
            self.header_frame,
            text=f" {'Price':<11} {'Amount'}",
            font=("Consolas", 10, "bold"),
            style="Card.TLabel",
            anchor=tk.W
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.ask_frame = ttk.Frame(self.right_frame, style="Order.TFrame")
        self.ask_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.bid_frame = ttk.Frame(self.right_frame, style="Order.TFrame")
        self.bid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        self.mapping = {
            "BTC/USDT": "btcusdt",
            "ETH/USDT": "ethusdt",
            "SOL/USDT": "solusdt",
            "LINK/USDT": "linkusdt",
            "XRP/USDT": "xrpusdt",
            "DOGE/USDT": "dogeusdt",
        }

        saved_coin = preferences.load_preference("selected_coin", "BTC/USDT")
        if saved_coin not in self.mapping:
            saved_coin = "BTC/USDT"
        self.choice.set(saved_coin)

        self.active_ticker = None
        self.active_order_book = None
        self.active_chart = None

        self.show_selected()

        if self.is_hidden:
            self.apply_hide_state()

    def toggle_show_hide(self):
        self.is_hidden = not self.is_hidden
        preferences.save_preference("is_hidden_info", self.is_hidden)
        if self.is_hidden:
            self.apply_hide_state()
            self.show_hide_btn.config(text="Show Info")
        else:
            self.show_info()
            self.show_hide_btn.config(text="Hide Info")

    def apply_hide_state(self):
        self.right_frame.pack_forget()
        if self.active_ticker:
            self.active_ticker.pack_forget()
        if self.active_order_book:
            self.active_order_book.pack_forget()

    def show_info(self):
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(20, 0))
        self.right_frame.config(width=200)
        self.right_frame.pack_propagate(False)
        if self.active_ticker:
            self.active_ticker.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        if self.active_order_book:
            self.active_order_book.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def on_coin_change(self, event=None):
        self.show_selected()
        preferences.save_preference("selected_coin", self.choice.get())
        if self.is_hidden:
            self.apply_hide_state()

    def show_selected(self, event=None):
        selection = self.choice.get()
        symbol = self.mapping[selection]
        self.title_label.config(text=f"{selection} DASHBOARD")

        for obj in [self.active_ticker, self.active_order_book, self.active_chart]:
            if obj:
                obj.stop()
                obj.pack_forget()

        self.active_ticker = CryptoTicker(self.left_frame, symbol)
        self.active_order_book = OrderBook(self.ask_frame, self.bid_frame, symbol)
        self.active_chart = PriceVolumeChart(self.chart_frame, symbol)

        self.active_ticker.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.active_order_book.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.active_chart.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.active_ticker.start()
        self.active_order_book.start()
        self.active_chart.start()

        if self.is_hidden:
            self.apply_hide_state()

    def on_closing(self):
        for obj in [self.active_ticker, self.active_order_book, self.active_chart]:
            if obj:
                obj.stop()
        self.root.after(300, self.root.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    app = TickerApp(root)
    root.minsize(1000, 762)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
