import tkinter as tk
from tkinter import ttk
from components.ticker import CryptoTicker
from components.order_book import OrderBook
from components.chart import PriceVolumeChart


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

        self.btc_chart = PriceVolumeChart(self.chart_frame, "btcusdt")
        self.eth_chart = PriceVolumeChart(self.chart_frame, "ethusdt")
        self.sol_chart = PriceVolumeChart(self.chart_frame, "solusdt")
        self.link_chart = PriceVolumeChart(self.chart_frame, "linkusdt")
        self.xrp_chart = PriceVolumeChart(self.chart_frame, "xrpusdt")
        self.doge_chart = PriceVolumeChart(self.chart_frame, "dogeusdt")

        self.btc_chart.pack(fill=tk.BOTH, expand=True)
        self.btc_chart.start()

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
            "BTC/USDT": (self.btc_ticker, self.btc_order_book, self.btc_chart),
            "ETH/USDT": (self.eth_ticker, self.eth_order_book, self.eth_chart),
            "SOL/USDT": (self.sol_ticker, self.sol_order_book, self.sol_chart),
            "LINK/USDT": (self.link_ticker, self.link_order_book, self.link_chart),
            "XRP/USDT": (self.xrp_ticker, self.xrp_order_book, self.xrp_chart),
            "DOGE/USDT": (self.doge_ticker, self.doge_order_book, self.doge_chart),
        }

        for ticker, order_book, chart in mapping.values():
            ticker.stop()
            ticker.pack_forget()

            order_book.stop()
            order_book.pack_forget()

            chart.stop()
            chart.pack_forget()

        chosen_ticker, chosen_order_book, chosen_chart = mapping[selection]

        chosen_ticker.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        chosen_ticker.start()

        chosen_order_book.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        chosen_order_book.start()

        chosen_chart.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        chosen_chart.start()

    def on_closing(self):
        mapping = {
            "BTC/USDT": (self.btc_ticker, self.btc_order_book, self.btc_chart),
            "ETH/USDT": (self.eth_ticker, self.eth_order_book, self.eth_chart),
            "SOL/USDT": (self.sol_ticker, self.sol_order_book, self.sol_chart),
            "LINK/USDT": (self.link_ticker, self.link_order_book, self.link_chart),
            "XRP/USDT": (self.xrp_ticker, self.xrp_order_book, self.xrp_chart),
            "DOGE/USDT": (self.doge_ticker, self.doge_order_book, self.doge_chart),
        }

        for ticker, order_book, chart in mapping.values():
            ticker.stop()
            order_book.stop()
            chart.stop()

        self.root.after(300, self.root.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    app = TickerApp(root)
    root.minsize(1000, 762)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
