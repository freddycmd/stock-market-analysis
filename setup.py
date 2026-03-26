from setuptools import setup, find_packages

setup(
    name="stock-market-analysis",
    version="0.1.0",
    description="Stock market data analysis with Python and pandas",
    author="freddycmd",
    url="https://github.com/freddycmd/stock-market-analysis",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "yfinance>=0.2.18",
        "plotly>=5.15.0",
        "scipy>=1.10.0",
        "ta>=0.10.2",
    ],
)
