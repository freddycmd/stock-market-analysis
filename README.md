# 📈 Stock Market Analysis

A Python-based stock market data analysis project using pandas, matplotlib, and seaborn.

## Project Structure

```
stock-market-analysis/
├── data/
│   ├── raw/              # Original, unmodified datasets
│   └── processed/        # Cleaned and transformed data
├── notebooks/            # Jupyter notebooks for exploration
├── src/                  # Source code / modules
├── reports/
│   └── figures/          # Generated charts and visualizations
├── tests/                # Unit tests
├── requirements.txt      # Python dependencies
├── setup.py              # Package setup
└── README.md
```

## Setup

```bash
# Clone the repo
git clone https://github.com/freddycmd/stock-market-analysis.git
cd stock-market-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

## Features

- **Data Collection**: Fetch historical stock data via yfinance
- **Exploratory Analysis**: Price trends, volume, returns distribution
- **Technical Indicators**: Moving averages, RSI, MACD, Bollinger Bands
- **Visualization**: Interactive and static charts
- **Interactive Dashboards**: Plotly candlestick, technical dashboard, returns heatmap, volume profile
- **Advanced Charts**: Drawdown, rolling volatility, weekday returns, monthly performance, event annotations
- **Statistical Analysis**: Correlation, volatility, risk metrics

## Usage

```python
from src.data_loader import StockDataLoader
from src.analysis import StockAnalyzer
from src.visualizer import StockVisualizer

# Load data
loader = StockDataLoader()
df = loader.fetch("AAPL", start="2020-01-01", end="2025-12-31")

# Analyze
analyzer = StockAnalyzer(df)
analyzer.add_moving_averages([20, 50, 200])
analyzer.add_rsi()
analyzer.add_macd()

# Visualize
viz = StockVisualizer(df)
viz.plot_price_with_ma()
viz.plot_volume()
viz.plot_returns_distribution()
```

## Notebooks

| Notebook | Description |
|----------|-------------|
| `01_data_exploration.ipynb` | Initial data loading and EDA |
| `02_technical_analysis.ipynb` | Technical indicators and signals |
| `03_portfolio_analysis.ipynb` | Multi-stock comparison and portfolio metrics |
| `04_dashboards.ipynb` | Interactive Plotly dashboards and advanced charts |

## License

MIT
