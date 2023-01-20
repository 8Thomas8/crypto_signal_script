import os
import requests
import json
import ccxt
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

os.system('')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Initialize the Binance exchange object
binance = ccxt.binance({
    'rateLimit': 2000,
    'enableRateLimit': True,
    'verbose': False,
    'apiKey': os.getenv('API_KEY'),
    'secret': os.getenv('API_SECRET'),
    'options': {
        'adjustForTimeDifference': True,
        'defaultType': 'spot'
    }
})

binanceData = {}

utArray = ['5m', '15m', '30m', '1h', '4h', '1d', '1w']
pairArray = ['BTC/BUSD','ETH/BUSD']
for i in pairArray :
    print(bcolors.OKBLUE + "================================ " + i + " - BINANCE ================================" + bcolors.ENDC)
    for j in utArray :
        # Get historical data for Ethereum on Binance
        ohlcv= binance.fetch_ohlcv(i, j)

        # Extract the close prices and calculate the indicators
        data = {}
        data['close'] = [x[4] for x in ohlcv]
        df = pd.DataFrame(data)
        sma20 = df["close"].rolling(window=20).mean()
        delta = df["close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        macd = df["close"].ewm(span=12, adjust=False).mean() - df["close"].ewm(span=26, adjust=False).mean()
        signal = macd.ewm(span=9, adjust=False).mean()

        # Generate the buy and sell signals
        print("------ " + i + " - BINANCE - " + " Unité de temps : " + j + " ------")

        if (df["close"].iloc[-1] > sma20.iloc[-1]) and (rsi.iloc[-1] > 70) and (macd.iloc[-1] > signal.iloc[-1]):
            print(bcolors.OKGREEN + "------ " + "Signal d'achat fort" + bcolors.ENDC)
        elif (df["close"].iloc[-1] > sma20.iloc[-1]) and (rsi.iloc[-1] > 50) and (macd.iloc[-1] > signal.iloc[-1]):
            print(bcolors.WARNING + "------ " + "Signal d'achat modéré" + bcolors.ENDC)
        elif (df["close"].iloc[-1] < sma20.iloc[-1]) and (rsi.iloc[-1] < 30) and (macd.iloc[-1] < signal.iloc[-1]):
            print(bcolors.FAIL + "------ " + "Signal de vente fort" + bcolors.ENDC)
        elif (df["close"].iloc[-1] < sma20.iloc[-1]) and (rsi.iloc[-1] < 50) and (macd.iloc[-1] < signal.iloc[-1]):
            print(bcolors.WARNING + "------ " + "Signal de vente modéré" + bcolors.ENDC)
        else:
            print("------ " + "Pas de signal")

        print("---------------------------------")
print(bcolors.OKBLUE + "==================================================================================" + bcolors.ENDC)
