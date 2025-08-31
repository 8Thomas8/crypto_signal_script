# Crypto Signal Script

This Python script analyzes cryptocurrency pairs on Binance using technical indicators (SMA20, RSI, MACD) and generates buy/sell signals.

## Features

- Retrieves historical data for selected pairs and timeframes from Binance
- Calculates SMA20, RSI, and MACD indicators
- Displays strong or moderate buy/sell signals based on indicators
- Supports multiple pairs and timeframes
- Colored output for easy reading

## Prerequisites

- Python 3.8+
- [ccxt](https://github.com/ccxt/ccxt)
- pandas
- python-dotenv
- requests

Dependency installation:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file at the root of your project with the following content:

- `UT_ARRAY`: Comma-separated list of timeframes.
- `PAIR_ARRAY`: Comma-separated list of trading pairs.
- `API_KEY` and `API_SECRET`: Your Binance API credentials.

The script automatically loads these variables for its configuration

## Usage

Run the script:

```bash
python signal_sma20_rsi_macd.py
```

## Disclaimer

This script is provided for educational purposes. Use it at your own risk. Always do your own research before investing.

## License

MIT License
