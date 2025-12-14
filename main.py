import tkinter as tk
from tkinter import ttk
from components.ticker import CryptoTicker
from components.order_book import OrderBook


class TickerApp:
    BG = "#0f0f0f"
    CARD_BG = "#1a1a1a"
    CARD_BORDER = "#262626"
    TEXT_MAIN = "#ffffff"
    TEXT_SUB = "#c7c7c7"
    DARK_BOX = "#111418"
    ORDER_BOX = "#282828"

    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Binance Dashboard")
        self.root.geometry("1000x600")
        root.configure(bg=self.BG)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=self.BG)
        style.configure("Card.TFrame", background=self.CARD_BG, bordercolor=self.CARD_BORDER)
        style.configure("TLabel", background=self.BG, foreground=self.TEXT_MAIN)
        style.configure("Card.TLabel", background=self.CARD_BG, foreground=self.TEXT_MAIN)
        style.configure("Small.TLabel", background=self.CARD_BG, foreground=self.TEXT_SUB)
        style.configure("Order.TFrame", background=self.ORDER_BOX)

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
        self.combo.current(0)
        self.combo.pack(side=tk.LEFT, pady=(5, 0))
        self.combo.bind("<<ComboboxSelected>>", self.show_selected)

        self.main_frame = ttk.Frame(self.root, style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.left_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(20, 0))
        self.right_frame.config(width=200)
        self.right_frame.pack_propagate(False)

        self.chart_frame = ttk.Frame(self.left_frame, style="Card.TFrame")
        self.chart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        self.btc_ticker = CryptoTicker(self.left_frame, "btcusdt")
        self.eth_ticker = CryptoTicker(self.left_frame, "ethusdt")
        self.sol_ticker = CryptoTicker(self.left_frame, "solusdt")
        self.link_ticker = CryptoTicker(self.left_frame, "linkusdt")
        self.xrp_ticker = CryptoTicker(self.left_frame, "xrpusdt")
        self.doge_ticker = CryptoTicker(self.left_frame, "dogeusdt")
        
        self.btc_ticker.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.btc_ticker.start()

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

        ttk.Label(self.header_frame, text=f" {"Price":<11} {"Amount"}",font=("Consolas", 10, "bold"), style="Card.TLabel", anchor=tk.W).pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.ask_frame = ttk.Frame(self.right_frame, style="Order.TFrame")
        self.ask_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.bid_frame = ttk.Frame(self.right_frame, style="Order.TFrame")
        self.bid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        self.btc_order_book = OrderBook(self.ask_frame, self.bid_frame,"btcusdt")
        self.eth_order_book = OrderBook(self.ask_frame, self.bid_frame,"ethusdt")
        self.sol_order_book = OrderBook(self.ask_frame, self.bid_frame,"solusdt")
        self.link_order_book = OrderBook(self.ask_frame, self.bid_frame,"linkusdt")
        self.xrp_order_book = OrderBook(self.ask_frame, self.bid_frame,"xrpusdt")
        self.doge_order_book = OrderBook(self.ask_frame, self.bid_frame,"dogeusdt")

        self.btc_order_book.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.btc_order_book.start()

    def show_selected(self, event=None):
        selection = self.choice.get()
        self.title_label.config(text=f"{selection} DASHBOARD")

        mapping = {
            "BTC/USDT": (self.btc_ticker, self.btc_order_book),
            "ETH/USDT": (self.eth_ticker, self.eth_order_book),
            "SOL/USDT": (self.sol_ticker, self.sol_order_book),
            "LINK/USDT": (self.link_ticker, self.link_order_book),
            "XRP/USDT": (self.xrp_ticker, self.xrp_order_book),
            "DOGE/USDT": (self.doge_ticker, self.doge_order_book)
        }

        for ticker, order_book in mapping.values():
            ticker.stop()
            ticker.pack_forget()

            order_book.stop()
            order_book.pack_forget()

        chosen_ticker = mapping[selection][0]
        chosen_order_book = mapping[selection][1]

        chosen_ticker.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        chosen_ticker.start()

        chosen_order_book.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        chosen_order_book.start()

    def on_closing(self):
        mapping = {
            "BTC/USDT": (self.btc_ticker, self.btc_order_book),
            "ETH/USDT": (self.eth_ticker, self.eth_order_book),
            "SOL/USDT": (self.sol_ticker, self.sol_order_book),
            "LINK/USDT": (self.link_ticker, self.link_order_book),
            "XRP/USDT": (self.xrp_ticker, self.xrp_order_book),
            "DOGE/USDT": (self.doge_ticker, self.doge_order_book)
        }

        for ticker, order_book in mapping.values():
            ticker.stop()
            order_book.stop()

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TickerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
