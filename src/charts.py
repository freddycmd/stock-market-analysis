"""Advanced chart types for stock analysis."""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc  # type: ignore
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional

sns.set_theme(style="darkgrid")


class AdvancedCharts:
    """Additional chart types beyond basic visualizations."""

    def __init__(self, df: pd.DataFrame, ticker: str = "Stock"):
        self.df = df.copy()
        self.ticker = ticker
        self.fig_dir = "reports/figures"

    def plot_drawdown(self, save: bool = True) -> plt.Figure:
        """Plot drawdown chart showing peak-to-trough declines."""
        cumulative = (1 + self.df["Close"].pct_change().fillna(0)).cumprod()
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak * 100

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), height_ratios=[2, 1])

        ax1.plot(self.df.index, self.df["Close"], linewidth=1.5, color="#2196F3")
        ax1.set_title(f"{self.ticker} — Price & Drawdown", fontsize=14, fontweight="bold")
        ax1.set_ylabel("Price ($)")

        ax2.fill_between(self.df.index, drawdown, 0, color="#F44336", alpha=0.4)
        ax2.plot(self.df.index, drawdown, color="#F44336", linewidth=0.8)
        ax2.set_ylabel("Drawdown (%)")
        ax2.set_xlabel("Date")

        plt.tight_layout()
        if save:
            fig.savefig(f"{self.fig_dir}/{self.ticker}_drawdown.png", dpi=150)
        return fig

    def plot_rolling_volatility(
        self, windows: list[int] = [21, 63], save: bool = True
    ) -> plt.Figure:
        """Plot rolling annualized volatility."""
        fig, ax = plt.subplots(figsize=(14, 6))
        returns = self.df["Close"].pct_change()
        colors = ["#2196F3", "#FF9800", "#E91E63", "#4CAF50"]

        for i, w in enumerate(windows):
            vol = returns.rolling(window=w).std() * np.sqrt(252) * 100
            label = f"{w}-day ({w // 21}mo)" if w >= 21 else f"{w}-day"
            ax.plot(self.df.index, vol, label=label,
                    linewidth=1.5, color=colors[i % len(colors)])

        ax.set_title(
            f"{self.ticker} — Rolling Annualized Volatility",
            fontsize=14, fontweight="bold",
        )
        ax.set_ylabel("Volatility (%)")
        ax.legend()
        plt.tight_layout()
        if save:
            fig.savefig(f"{self.fig_dir}/{self.ticker}_volatility.png", dpi=150)
        return fig

    def plot_daily_returns_by_weekday(self, save: bool = True) -> plt.Figure:
        """Box plot of returns by day of the week."""
        df = self.df.copy()
        df["Return"] = df["Close"].pct_change() * 100
        df["Weekday"] = df.index.day_name()

        order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        df = df.dropna(subset=["Return"])

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(
            data=df, x="Weekday", y="Return", order=order,
            palette="Set2", showfliers=False, ax=ax,
        )
        ax.axhline(0, color="gray", linestyle="--", alpha=0.5)
        ax.set_title(
            f"{self.ticker} — Daily Returns by Weekday",
            fontsize=14, fontweight="bold",
        )
        ax.set_ylabel("Daily Return (%)")
        ax.set_xlabel("")
        plt.tight_layout()
        if save:
            fig.savefig(f"{self.fig_dir}/{self.ticker}_weekday_returns.png", dpi=150)
        return fig

    def plot_monthly_performance(self, save: bool = True) -> plt.Figure:
        """Bar chart of average monthly returns."""
        df = self.df.copy()
        df["Return"] = df["Close"].pct_change()
        df["Month"] = df.index.month

        monthly_avg = df.groupby("Month")["Return"].mean() * 100
        month_names = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
        ]

        fig, ax = plt.subplots(figsize=(12, 6))
        colors = ["#4CAF50" if v >= 0 else "#F44336" for v in monthly_avg]
        ax.bar(range(1, 13), monthly_avg, color=colors, alpha=0.8, edgecolor="white")
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(month_names)
        ax.axhline(0, color="gray", linestyle="-", linewidth=0.5)
        ax.set_title(
            f"{self.ticker} — Average Monthly Returns",
            fontsize=14, fontweight="bold",
        )
        ax.set_ylabel("Avg Daily Return (%)")
        plt.tight_layout()
        if save:
            fig.savefig(f"{self.fig_dir}/{self.ticker}_monthly_perf.png", dpi=150)
        return fig

    def plot_cumulative_returns_comparison(
        self, others: dict[str, pd.DataFrame], save: bool = True
    ) -> plt.Figure:
        """Compare cumulative returns of multiple stocks."""
        fig, ax = plt.subplots(figsize=(14, 6))
        all_stocks = {self.ticker: self.df, **others}
        colors = [
            "#2196F3", "#FF9800", "#E91E63", "#4CAF50",
            "#9C27B0", "#00BCD4", "#FF5722",
        ]

        for i, (ticker, df) in enumerate(all_stocks.items()):
            cum_ret = (1 + df["Close"].pct_change().fillna(0)).cumprod()
            cum_ret = (cum_ret - 1) * 100
            ax.plot(df.index, cum_ret, label=ticker,
                    linewidth=1.5, color=colors[i % len(colors)])

        ax.axhline(0, color="gray", linestyle="--", alpha=0.5)
        ax.set_title("Cumulative Returns Comparison", fontsize=14, fontweight="bold")
        ax.set_ylabel("Cumulative Return (%)")
        ax.legend()
        plt.tight_layout()
        if save:
            fig.savefig(f"{self.fig_dir}/cumulative_comparison.png", dpi=150)
        return fig

    def plot_price_with_events(
        self, events: list[dict], save: bool = True
    ) -> plt.Figure:
        """
        Price chart with annotated events.

        Args:
            events: list of {"date": "YYYY-MM-DD", "label": "text"}
        """
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(self.df.index, self.df["Close"], linewidth=1.5, color="#2196F3")

        for event in events:
            date = pd.Timestamp(event["date"])
            if date in self.df.index:
                price = self.df.loc[date, "Close"]
            else:
                nearest = self.df.index[self.df.index.get_indexer([date], method="nearest")[0]]
                price = self.df.loc[nearest, "Close"]
                date = nearest

            ax.annotate(
                event["label"],
                xy=(date, price),
                xytext=(0, 30),
                textcoords="offset points",
                arrowprops=dict(arrowstyle="->", color="#FF9800"),
                fontsize=9,
                ha="center",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#FF9800", alpha=0.3),
            )

        ax.set_title(
            f"{self.ticker} — Price with Events", fontsize=14, fontweight="bold"
        )
        ax.set_ylabel("Price ($)")
        plt.tight_layout()
        if save:
            fig.savefig(f"{self.fig_dir}/{self.ticker}_events.png", dpi=150)
        return fig
