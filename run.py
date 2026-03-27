"""Run the stock market analysis and generate all outputs."""

import sys
sys.path.insert(0, ".")

from src.data_loader import StockDataLoader
from src.analysis import StockAnalyzer
from src.dashboard import StockDashboard
from src.charts import AdvancedCharts

def main():
    print("=" * 60)
    print("📈 Stock Market Analysis")
    print("=" * 60)

    # Load data
    loader = StockDataLoader(cache_dir="data/raw")
    ticker = "AAPL"

    print(f"\n🔄 Fetching {ticker} data...")
    df = loader.fetch(ticker, start="2020-01-01")
    print(f"✅ Loaded {len(df)} rows ({df.index.min().date()} to {df.index.max().date()})")

    # Analysis
    print(f"\n📊 Running technical analysis...")
    analyzer = StockAnalyzer(df)
    analyzer.add_moving_averages([20, 50, 200])
    analyzer.add_ema([12, 26])
    analyzer.add_rsi()
    analyzer.add_macd()
    analyzer.add_bollinger_bands()
    analyzer.add_volume_sma()
    enriched = analyzer.get_data()

    # Summary stats
    stats = analyzer.summary_stats()
    print(f"\n📋 {ticker} Summary:")
    print(f"   Total Return:          {stats['total_return']*100:>8.2f}%")
    print(f"   Annualized Return:     {stats['annualized_return']*100:>8.2f}%")
    print(f"   Annualized Volatility: {stats['annualized_volatility']*100:>8.2f}%")
    print(f"   Sharpe Ratio:          {stats['sharpe_ratio']:>8.4f}")
    print(f"   Max Drawdown:          {stats['max_drawdown']*100:>8.2f}%")
    print(f"   Best Day:              {stats['best_day']*100:>8.2f}%")
    print(f"   Worst Day:             {stats['worst_day']*100:>8.2f}%")
    print(f"   Positive Days:         {stats['positive_days_pct']:>8.2f}%")

    # Generate static charts
    print(f"\n🎨 Generating static charts...")
    from src.visualizer import StockVisualizer
    viz = StockVisualizer(enriched, ticker=ticker)
    viz.plot_price()
    viz.plot_price_with_ma()
    viz.plot_volume()
    viz.plot_returns_distribution()
    viz.plot_rsi()
    viz.plot_macd()
    print("✅ Saved to reports/figures/")

    # Generate advanced charts
    print(f"\n🎨 Generating advanced charts...")
    charts = AdvancedCharts(enriched, ticker=ticker)
    charts.plot_drawdown()
    charts.plot_rolling_volatility()
    charts.plot_daily_returns_by_weekday()
    charts.plot_monthly_performance()
    print("✅ Saved to reports/figures/")

    # Generate interactive dashboard
    print(f"\n🖥️  Generating interactive dashboards...")
    dash = StockDashboard(enriched, ticker=ticker)
    fig_candle = dash.candlestick_chart(last_n_days=120)
    dash.save_html(fig_candle, f"{ticker}_candlestick.html")
    fig_tech = dash.technical_dashboard()
    dash.save_html(fig_tech, f"{ticker}_technical_dashboard.html")
    fig_heatmap = dash.returns_heatmap()
    dash.save_html(fig_heatmap, f"{ticker}_returns_heatmap.html")
    fig_volume = dash.volume_profile(bins=60)
    dash.save_html(fig_volume, f"{ticker}_volume_profile.html")

    # Multi-stock comparison
    print(f"\n🔀 Loading comparison stocks...")
    compare_tickers = ["MSFT", "GOOGL", "AMZN", "TSLA"]
    others = {}
    for t in compare_tickers:
        others[t] = loader.fetch(t, start="2020-01-01")
        print(f"   ✅ {t}: {len(others[t])} rows")

    fig_compare = dash.comparison_chart(others)
    dash.save_html(fig_compare, "stock_comparison.html")

    # Compare stats
    print(f"\n📋 All Stocks Summary:")
    print(f"{'Ticker':>8} {'Return':>10} {'Volatility':>12} {'Sharpe':>8} {'MaxDD':>8}")
    print("-" * 50)
    all_stocks = {ticker: df, **others}
    for t, d in all_stocks.items():
        a = StockAnalyzer(d)
        s = a.summary_stats()
        print(f"{t:>8} {s['total_return']*100:>9.2f}% {s['annualized_volatility']*100:>10.2f}% {s['sharpe_ratio']:>8.4f} {s['max_drawdown']*100:>7.2f}%")

    print(f"\n✅ Done! Check reports/ for all outputs.")
    print(f"   📊 Static charts: reports/figures/*.png")
    print(f"   🖥️  Dashboards:    reports/*.html")

if __name__ == "__main__":
    main()
