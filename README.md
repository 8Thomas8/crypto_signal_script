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

Create a `.env` file at the root of the project with your Binance credentials:

```
API_KEY=your_binance_api_key
API_SECRET=your_binance_api_secret
```

## Usage

Run the script:

```bash
python signal_sma20_rsi_macd.py
```

## Customization

Edit `pairArray` in `signal_sma20_rsi_macd.py` to change the pairs.
Edit `utArray` to change the timeframes.

## Disclaimer

This script is provided for educational purposes. Use it at your own risk. Always do your own research before investing.

## License

MIT License
