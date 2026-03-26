"""Interactive dashboard module using Plotly."""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Optional


class StockDashboard:
    """Interactive stock market dashboards with Plotly."""

    def __init__(self, df: pd.DataFrame, ticker: str = "Stock"):
        self.df = df.copy()
        self.ticker = ticker

    def candlestick_chart(
        self, last_n_days: Optional[int] = None, show_volume: bool = True
    ) -> go.Figure:
        """
        Interactive candlestick chart with volume bars.

        Args:
            last_n_days: Show only last N trading days (None = all)
            show_volume: Include volume subplot
        """
        data = self.df.tail(last_n_days) if last_n_days else self.df

        if show_volume:
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.03,
                row_heights=[0.7, 0.3],
                subplot_titles=(f"{self.ticker} — Price", "Volume"),
            )
        else:
            fig = make_subplots(rows=1, cols=1)

        # Candlestick
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                name="OHLC",
                increasing_line_color="#26A69A",
                decreasing_line_color="#EF5350",
            ),
            row=1, col=1,
        )

        # Moving averages if present
        ma_colors = {"SMA_20": "#FF9800", "SMA_50": "#E91E63", "SMA_200": "#2196F3"}
        for col, color in ma_colors.items():
            if col in data.columns:
                fig.add_trace(
                    go.Scatter(
                        x=data.index, y=data[col],
                        name=col, line=dict(width=1, color=color),
                    ),
                    row=1, col=1,
                )

        # Volume
        if show_volume:
            colors = [
                "#26A69A" if c >= o else "#EF5350"
                for c, o in zip(data["Close"], data["Open"])
            ]
            fig.add_trace(
                go.Bar(
                    x=data.index, y=data["Volume"],
                    name="Volume", marker_color=colors, opacity=0.7,
                ),
                row=2, col=1,
            )

        fig.update_layout(
            title=f"{self.ticker} — Candlestick Chart",
            xaxis_rangeslider_visible=False,
            template="plotly_dark",
            height=700,
            showlegend=True,
            legend=dict(x=0, y=1.12, orientation="h"),
        )
        return fig

    def technical_dashboard(self) -> go.Figure:
        """
        Full technical analysis dashboard:
        Price + MAs, Volume, RSI, MACD — all in one view.
        """
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.02,
            row_heights=[0.4, 0.15, 0.2, 0.25],
            subplot_titles=(
                f"{self.ticker} — Price",
                "Volume",
                "RSI",
                "MACD",
            ),
        )

        # Row 1: Candlestick + Bollinger Bands
        fig.add_trace(
            go.Candlestick(
                x=self.df.index,
                open=self.df["Open"],
                high=self.df["High"],
                low=self.df["Low"],
                close=self.df["Close"],
                name="OHLC",
                increasing_line_color="#26A69A",
                decreasing_line_color="#EF5350",
            ),
            row=1, col=1,
        )

        if "BB_Upper" in self.df.columns:
            fig.add_trace(
                go.Scatter(
                    x=self.df.index, y=self.df["BB_Upper"],
                    name="BB Upper", line=dict(width=1, color="#9C27B0", dash="dot"),
                ),
                row=1, col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=self.df.index, y=self.df["BB_Lower"],
                    name="BB Lower", line=dict(width=1, color="#9C27B0", dash="dot"),
                    fill="tonexty", fillcolor="rgba(156, 39, 176, 0.1)",
                ),
                row=1, col=1,
            )

        ma_colors = {"SMA_20": "#FF9800", "SMA_50": "#E91E63", "SMA_200": "#2196F3"}
        for col, color in ma_colors.items():
            if col in self.df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=self.df.index, y=self.df[col],
                        name=col, line=dict(width=1, color=color),
                    ),
                    row=1, col=1,
                )

        # Row 2: Volume
        colors = [
            "#26A69A" if c >= o else "#EF5350"
            for c, o in zip(self.df["Close"], self.df["Open"])
        ]
        fig.add_trace(
            go.Bar(
                x=self.df.index, y=self.df["Volume"],
                name="Volume", marker_color=colors, opacity=0.7,
            ),
            row=2, col=1,
        )

        # Row 3: RSI
        if "RSI" in self.df.columns:
            fig.add_trace(
                go.Scatter(
                    x=self.df.index, y=self.df["RSI"],
                    name="RSI", line=dict(width=1.5, color="#9C27B0"),
                ),
                row=3, col=1,
            )
            fig.add_hline(y=70, line_dash="dash", line_color="#F44336", opacity=0.5, row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="#4CAF50", opacity=0.5, row=3, col=1)
            fig.update_yaxes(range=[0, 100], row=3, col=1)

        # Row 4: MACD
        if "MACD" in self.df.columns:
            fig.add_trace(
                go.Scatter(
                    x=self.df.index, y=self.df["MACD"],
                    name="MACD", line=dict(width=1.5, color="#2196F3"),
                ),
                row=4, col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=self.df.index, y=self.df["MACD_Signal"],
                    name="Signal", line=dict(width=1.5, color="#FF9800"),
                ),
                row=4, col=1,
            )
            hist_colors = [
                "#26A69A" if v >= 0 else "#EF5350"
                for v in self.df["MACD_Hist"]
            ]
            fig.add_trace(
                go.Bar(
                    x=self.df.index, y=self.df["MACD_Hist"],
                    name="MACD Hist", marker_color=hist_colors, opacity=0.6,
                ),
                row=4, col=1,
            )

        fig.update_layout(
            template="plotly_dark",
            height=1000,
            showlegend=True,
            legend=dict(x=0, y=1.05, orientation="h"),
            xaxis4_rangeslider_visible=False,
            xaxis_rangeslider_visible=False,
        )
        return fig

    def returns_heatmap(self) -> go.Figure:
        """Monthly returns heatmap."""
        df = self.df.copy()
        df["Year"] = df.index.year
        df["Month"] = df.index.month

        monthly = df.groupby(["Year", "Month"])["Close"].last().unstack()
        monthly_returns = monthly.pct_change(axis=1)

        # Recalculate properly: month-over-month
        monthly_close = df.groupby([df.index.year, df.index.month])["Close"].last()
        monthly_ret = monthly_close.pct_change()
        pivot = monthly_ret.unstack(level=1)
        pivot.columns = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
        ]

        fig = go.Figure(
            data=go.Heatmap(
                z=pivot.values * 100,
                x=pivot.columns,
                y=pivot.index.astype(str),
                colorscale="RdYlGn",
                zmid=0,
                text=np.round(pivot.values * 100, 1),
                texttemplate="%{text:.1f}%",
                textfont=dict(size=11),
                colorbar=dict(title="Return %"),
            )
        )
        fig.update_layout(
            title=f"{self.ticker} — Monthly Returns Heatmap (%)",
            template="plotly_dark",
            height=400,
            yaxis=dict(autorange="reversed"),
        )
        return fig

    def comparison_chart(
        self, others: dict[str, pd.DataFrame], normalize: bool = True
    ) -> go.Figure:
        """
        Compare multiple stocks on one chart.

        Args:
            others: dict of {ticker: DataFrame}
            normalize: Normalize to base 100
        """
        fig = go.Figure()

        all_stocks = {self.ticker: self.df, **others}
        colors = [
            "#2196F3", "#FF9800", "#E91E63", "#4CAF50",
            "#9C27B0", "#00BCD4", "#FF5722", "#795548",
        ]

        for i, (ticker, df) in enumerate(all_stocks.items()):
            y = df["Close"]
            if normalize:
                y = y / y.iloc[0] * 100
            fig.add_trace(
                go.Scatter(
                    x=df.index, y=y,
                    name=ticker,
                    line=dict(width=2, color=colors[i % len(colors)]),
                )
            )

        fig.update_layout(
            title="Stock Comparison" + (" (Normalized)" if normalize else ""),
            template="plotly_dark",
            height=600,
            yaxis_title="Normalized Price" if normalize else "Price ($)",
            hovermode="x unified",
        )
        return fig

    def volume_profile(self, bins: int = 50) -> go.Figure:
        """Volume profile — price levels with most trading activity."""
        fig = make_subplots(
            rows=1, cols=2,
            shared_yaxes=True,
            column_widths=[0.7, 0.3],
            subplot_titles=(f"{self.ticker} — Price", "Volume Profile"),
        )

        fig.add_trace(
            go.Candlestick(
                x=self.df.index,
                open=self.df["Open"],
                high=self.df["High"],
                low=self.df["Low"],
                close=self.df["Close"],
                name="OHLC",
            ),
            row=1, col=1,
        )

        price_bins = np.linspace(self.df["Low"].min(), self.df["High"].max(), bins)
        vol_profile = np.zeros(len(price_bins) - 1)

        for _, row in self.df.iterrows():
            mask = (price_bins[:-1] >= row["Low"]) & (price_bins[1:] <= row["High"])
            vol_profile[mask] += row["Volume"] / max(mask.sum(), 1)

        bin_centers = (price_bins[:-1] + price_bins[1:]) / 2

        fig.add_trace(
            go.Bar(
                x=vol_profile, y=bin_centers,
                orientation="h", name="Volume Profile",
                marker_color="#2196F3", opacity=0.6,
            ),
            row=1, col=2,
        )

        fig.update_layout(
            template="plotly_dark",
            height=700,
            xaxis_rangeslider_visible=False,
            showlegend=False,
        )
        return fig

    def save_html(self, fig: go.Figure, filename: str):
        """Save a Plotly figure as an interactive HTML file."""
        path = f"reports/{filename}"
        fig.write_html(path, include_plotlyjs="cdn")
        print(f"Saved: {path}")
        return path
