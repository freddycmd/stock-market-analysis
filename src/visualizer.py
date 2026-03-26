"""Stock visualization module."""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
from typing import Optional

sns.set_theme(style="darkgrid")


class StockVisualizer:
    """Create stock market charts and visualizations."""

    def __init__(self, df: pd.DataFrame, ticker: str = "Stock"):
        self.df = df.copy()
        self.ticker = ticker
        self.fig_dir = "reports/figures"

    def plot_price(self, save: bool = True) -> plt.Figure:
        """Plot closing price over time."""
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(self.df.index, self.df["Close"], linewidth=1.5, color="#2196F3")
        ax.set_title(f"{self.ticker} — Closing Price", fontsize=14, fontweight="bold")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price ($)")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        plt.tight_layout()
        if save:
            fig.savefig(f"{self.fig_dir}/{self.ticker}_price.png", dpi=150)
        return fig

    def plot_price_with_ma(
        self, windows: list[int] = [20, 50, 200], save: bool = True
    ) -> plt.Figure:
        """Plot price with moving averages."""
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(self.df.index, self.df["Close"], label="Close", linewidth=1.5)
        colors = ["#FF9800", "#E91E63", "#4CAF50"]
        for i, w in enumerate(windows):
            col = f"SMA_{w}"
            if col in self.df.columns:
                ax.plot(
                    self.df.index,
                    self.df[col],
                    label=f"SMA {w}",
                    linewidth=1,
                    color=colors[i % len(colors)],
                )
        ax.set_title(
            f"{self.ticker} — Price & Moving Averages", fontsize=14, fontweight="bold"
        )
        ax.legend()
        ax.set_xlabel("Date")
        ax.set_ylabel("Price ($)")
        plt.tight_layout()
        if save:
            fig.savefig(f"{self.fig_dir}/{self.ticker}_price_ma.png", dpi=150)
        return fig

    def plot_volume(self, save: bool = True) -> plt.Figure:
        """Plot trading volume."""
        fig, ax = plt.subplots(figsize=(14, 4))
        colors = [
            "#4CAF50" if c >= o else "#F44336"
            for c, o in zip(self.df["Close"], self.df["Open"])
        ]
        ax.bar(self.df.index, self.df["Volume"], color=colors, alpha=0.7, width=1)
        if "Volume_SMA" in self.df.columns:
            ax.plot(
                self.df.index,
                self.df["Volume_SMA"],
                color="#FF9800",
                linewidth=1.5,
                label="Volume SMA",
            )
            ax.legend()
        ax.set_title(f"{self.ticker} — Trading Volume", fontsize=14, fontweight="bold")
        ax.set_xlabel("Date")
        ax.set_ylabel("Volume")
        plt.tight_layout()
        if save:
            fig.savefig(f"{self.fig_dir}/{self.ticker}_volume.png", dpi=150)
        return fig

    def plot_returns_distribution(self, save: bool = True) -> plt.Figure:
        """Plot daily returns distribution."""
        fig, ax = plt.subplots(figsize=(10, 6))
        returns = self.df["Daily_Return"].dropna()
        ax.hist(returns, bins=50, alpha=0.75, color="#2196F3", edgecolor="white")
        ax.axvline(returns.mean(), color="#F44336", linestyle="--", label=f"Mean: {returns.mean():.4f}")
        ax.axvline(0, color="black", linestyle="-", linewidth=0.5)
        ax.set_title(
            f"{self.ticker} — Daily Returns Distribution",
            fontsize=14,
            fontweight="bold",
        )
        ax.set_xlabel("Daily Return")
        ax.set_ylabel("Frequency")
        ax.legend()
        plt.tight_layout()
        if save:
            fig.savefig(f"{self.fig_dir}/{self.ticker}_returns_dist.png", dpi=150)
        return fig

    def plot_rsi(self, save: bool = True) -> plt.Figure:
        """Plot RSI indicator."""
        if "RSI" not in self.df.columns:
            raise ValueError("RSI not computed. Run analyzer.add_rsi() first.")

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), height_ratios=[3, 1])
        ax1.plot(self.df.index, self.df["Close"], linewidth=1.5)
        ax1.set_title(f"{self.ticker} — Price & RSI", fontsize=14, fontweight="bold")
        ax1.set_ylabel("Price ($)")

        ax2.plot(self.df.index, self.df["RSI"], color="#9C27B0", linewidth=1)
        ax2.axhline(70, color="#F44336", linestyle="--", alpha=0.7, label="Overbought (70)")
        ax2.axhline(30, color="#4CAF50", linestyle="--", alpha=0.7, label="Oversold (30)")
        ax2.fill_between(self.df.index, 70, 100, alpha=0.1, color="#F44336")
        ax2.fill_between(self.df.index, 0, 30, alpha=0.1, color="#4CAF50")
        ax2.set_ylim(0, 100)
        ax2.set_ylabel("RSI")
        ax2.legend(loc="upper left")
        plt.tight_layout()
        if save:
            fig.savefig(f"{self.fig_dir}/{self.ticker}_rsi.png", dpi=150)
        return fig

    def plot_macd(self, save: bool = True) -> plt.Figure:
        """Plot MACD indicator."""
        if "MACD" not in self.df.columns:
            raise ValueError("MACD not computed. Run analyzer.add_macd() first.")

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), height_ratios=[3, 1])
        ax1.plot(self.df.index, self.df["Close"], linewidth=1.5)
        ax1.set_title(f"{self.ticker} — Price & MACD", fontsize=14, fontweight="bold")
        ax1.set_ylabel("Price ($)")

        ax2.plot(self.df.index, self.df["MACD"], label="MACD", color="#2196F3")
        ax2.plot(self.df.index, self.df["MACD_Signal"], label="Signal", color="#FF9800")
        colors = ["#4CAF50" if v >= 0 else "#F44336" for v in self.df["MACD_Hist"]]
        ax2.bar(self.df.index, self.df["MACD_Hist"], color=colors, alpha=0.5, width=1)
        ax2.set_ylabel("MACD")
        ax2.legend()
        plt.tight_layout()
        if save:
            fig.savefig(f"{self.fig_dir}/{self.ticker}_macd.png", dpi=150)
        return fig
