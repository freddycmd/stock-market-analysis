"""Tests for stock analysis modules."""

import pytest
import pandas as pd
import numpy as np
from src.analysis import StockAnalyzer


@pytest.fixture
def sample_data():
    """Create sample OHLCV data for testing."""
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=100, freq="B")
    close = 100 + np.cumsum(np.random.randn(100) * 2)
    return pd.DataFrame(
        {
            "Open": close - np.random.rand(100),
            "High": close + np.abs(np.random.randn(100)),
            "Low": close - np.abs(np.random.randn(100)),
            "Close": close,
            "Volume": np.random.randint(1_000_000, 10_000_000, 100),
        },
        index=dates,
    )


class TestStockAnalyzer:
    def test_init_adds_returns(self, sample_data):
        analyzer = StockAnalyzer(sample_data)
        df = analyzer.get_data()
        assert "Daily_Return" in df.columns
        assert "Cumulative_Return" in df.columns

    def test_moving_averages(self, sample_data):
        analyzer = StockAnalyzer(sample_data)
        analyzer.add_moving_averages([10, 20])
        df = analyzer.get_data()
        assert "SMA_10" in df.columns
        assert "SMA_20" in df.columns
        assert df["SMA_10"].iloc[9:].notna().all()

    def test_ema(self, sample_data):
        analyzer = StockAnalyzer(sample_data)
        analyzer.add_ema([12, 26])
        df = analyzer.get_data()
        assert "EMA_12" in df.columns
        assert "EMA_26" in df.columns

    def test_rsi(self, sample_data):
        analyzer = StockAnalyzer(sample_data)
        analyzer.add_rsi()
        df = analyzer.get_data()
        assert "RSI" in df.columns
        rsi_valid = df["RSI"].dropna()
        assert (rsi_valid >= 0).all() and (rsi_valid <= 100).all()

    def test_macd(self, sample_data):
        analyzer = StockAnalyzer(sample_data)
        analyzer.add_macd()
        df = analyzer.get_data()
        assert "MACD" in df.columns
        assert "MACD_Signal" in df.columns
        assert "MACD_Hist" in df.columns

    def test_bollinger_bands(self, sample_data):
        analyzer = StockAnalyzer(sample_data)
        analyzer.add_bollinger_bands()
        df = analyzer.get_data()
        assert "BB_Upper" in df.columns
        assert "BB_Middle" in df.columns
        assert "BB_Lower" in df.columns
        valid = df.dropna(subset=["BB_Upper", "BB_Lower"])
        assert (valid["BB_Upper"] >= valid["BB_Lower"]).all()

    def test_summary_stats(self, sample_data):
        analyzer = StockAnalyzer(sample_data)
        stats = analyzer.summary_stats()
        assert "total_return" in stats
        assert "annualized_return" in stats
        assert "sharpe_ratio" in stats
        assert "max_drawdown" in stats
        assert stats["max_drawdown"] <= 0
