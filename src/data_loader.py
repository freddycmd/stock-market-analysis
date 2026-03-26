"""Stock data loader module using yfinance."""

import yfinance as yf
import pandas as pd
from typing import Optional


class StockDataLoader:
    """Fetch and cache historical stock market data."""

    def __init__(self, cache_dir: str = "data/raw"):
        self.cache_dir = cache_dir

    def fetch(
        self,
        ticker: str,
        start: str = "2020-01-01",
        end: Optional[str] = None,
        interval: str = "1d",
        save: bool = True,
    ) -> pd.DataFrame:
        """
        Fetch historical stock data.

        Args:
            ticker: Stock symbol (e.g., 'AAPL', 'MSFT')
            start: Start date (YYYY-MM-DD)
            end: End date (YYYY-MM-DD), defaults to today
            interval: Data interval ('1d', '1wk', '1mo')
            save: Whether to save raw data to CSV

        Returns:
            DataFrame with OHLCV data
        """
        stock = yf.Ticker(ticker)
        df = stock.history(start=start, end=end, interval=interval)

        if df.empty:
            raise ValueError(f"No data returned for {ticker}")

        df.index.name = "Date"
        df = df[["Open", "High", "Low", "Close", "Volume"]]

        if save:
            path = f"{self.cache_dir}/{ticker}_{interval}.csv"
            df.to_csv(path)
            print(f"Saved: {path}")

        return df

    def fetch_multiple(
        self,
        tickers: list[str],
        start: str = "2020-01-01",
        end: Optional[str] = None,
        interval: str = "1d",
    ) -> dict[str, pd.DataFrame]:
        """Fetch data for multiple tickers."""
        data = {}
        for ticker in tickers:
            try:
                data[ticker] = self.fetch(ticker, start, end, interval)
            except ValueError as e:
                print(f"Warning: {e}")
        return data

    def load_csv(self, path: str) -> pd.DataFrame:
        """Load a previously saved CSV."""
        df = pd.read_csv(path, index_col="Date", parse_dates=True)
        return df
