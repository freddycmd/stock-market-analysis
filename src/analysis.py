"""Stock analysis module with technical indicators."""

import pandas as pd
import numpy as np
from typing import Optional


class StockAnalyzer:
    """Compute technical indicators and statistical metrics."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self._add_returns()

    def _add_returns(self):
        """Add daily and cumulative returns."""
        self.df["Daily_Return"] = self.df["Close"].pct_change()
        self.df["Cumulative_Return"] = (1 + self.df["Daily_Return"]).cumprod() - 1

    def add_moving_averages(self, windows: list[int] = [20, 50, 200]) -> pd.DataFrame:
        """Add Simple Moving Averages."""
        for w in windows:
            self.df[f"SMA_{w}"] = self.df["Close"].rolling(window=w).mean()
        return self.df

    def add_ema(self, windows: list[int] = [12, 26]) -> pd.DataFrame:
        """Add Exponential Moving Averages."""
        for w in windows:
            self.df[f"EMA_{w}"] = self.df["Close"].ewm(span=w, adjust=False).mean()
        return self.df

    def add_rsi(self, period: int = 14) -> pd.DataFrame:
        """Add Relative Strength Index."""
        delta = self.df["Close"].diff()
        gain = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        self.df["RSI"] = 100 - (100 / (1 + rs))
        return self.df

    def add_macd(
        self, fast: int = 12, slow: int = 26, signal: int = 9
    ) -> pd.DataFrame:
        """Add MACD indicator."""
        ema_fast = self.df["Close"].ewm(span=fast, adjust=False).mean()
        ema_slow = self.df["Close"].ewm(span=slow, adjust=False).mean()
        self.df["MACD"] = ema_fast - ema_slow
        self.df["MACD_Signal"] = self.df["MACD"].ewm(span=signal, adjust=False).mean()
        self.df["MACD_Hist"] = self.df["MACD"] - self.df["MACD_Signal"]
        return self.df

    def add_bollinger_bands(self, window: int = 20, std: int = 2) -> pd.DataFrame:
        """Add Bollinger Bands."""
        sma = self.df["Close"].rolling(window=window).mean()
        rolling_std = self.df["Close"].rolling(window=window).std()
        self.df["BB_Upper"] = sma + (rolling_std * std)
        self.df["BB_Middle"] = sma
        self.df["BB_Lower"] = sma - (rolling_std * std)
        return self.df

    def add_volume_sma(self, window: int = 20) -> pd.DataFrame:
        """Add volume moving average."""
        self.df["Volume_SMA"] = self.df["Volume"].rolling(window=window).mean()
        return self.df

    def summary_stats(self) -> dict:
        """Compute summary statistics."""
        returns = self.df["Daily_Return"].dropna()
        return {
            "total_return": float(self.df["Cumulative_Return"].iloc[-1]),
            "annualized_return": float(returns.mean() * 252),
            "annualized_volatility": float(returns.std() * np.sqrt(252)),
            "sharpe_ratio": float(
                (returns.mean() * 252) / (returns.std() * np.sqrt(252))
            )
            if returns.std() > 0
            else 0,
            "max_drawdown": float(self._max_drawdown()),
            "best_day": float(returns.max()),
            "worst_day": float(returns.min()),
            "positive_days_pct": float((returns > 0).sum() / len(returns) * 100),
        }

    def _max_drawdown(self) -> float:
        """Calculate maximum drawdown."""
        cumulative = (1 + self.df["Daily_Return"].fillna(0)).cumprod()
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak
        return drawdown.min()

    def get_data(self) -> pd.DataFrame:
        """Return the enriched DataFrame."""
        return self.df
