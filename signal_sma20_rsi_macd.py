import os
import requests
import json
import ccxt
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import concurrent.futures
import numpy as np

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

os.system('')

utArray = os.getenv('UT_ARRAY').split(',')
pairArray = os.getenv('PAIR_ARRAY').split(',')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_signal_concise(pair, ut, score, signal_type, cross_msg):
    print(f"{bcolors.BOLD}{bcolors.OKBLUE}{pair}{bcolors.ENDC} {bcolors.YELLOW}| {ut}{bcolors.ENDC} {bcolors.OKBLUE}- BINANCE{bcolors.ENDC} | {cross_msg} {signal_type} {bcolors.OKCYAN}Score: {score}{bcolors.ENDC}")

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

for i in pairArray :
    print(bcolors.OKBLUE + "================================ " + bcolors.HEADER + i + bcolors.ENDC + " - " + bcolors.YELLOW + "BINANCE" + bcolors.OKBLUE + " ================================" + bcolors.ENDC)
    for j in utArray :
        try:
            # Get historical data for Ethereum on Binance
            ohlcv= binance.fetch_ohlcv(i, j)

            # Extract the close prices and calculate the indicators
            data = {
                'close': [x[4] for x in ohlcv],
                'volume': [x[5] for x in ohlcv]
            }
            df = pd.DataFrame(data)
            sma20 = df["close"].rolling(window=20).mean()
            sma50 = df["close"].rolling(window=50).mean()
            delta = df["close"].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(window=14).mean()
            avg_loss = loss.rolling(window=14).mean()
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            macd = df["close"].ewm(span=12, adjust=False).mean() - df["close"].ewm(span=26, adjust=False).mean()
            signal = macd.ewm(span=9, adjust=False).mean()
            cross_up = sma20.iloc[-2] < sma50.iloc[-2] and sma20.iloc[-1] > sma50.iloc[-1]
            cross_down = sma20.iloc[-2] > sma50.iloc[-2] and sma20.iloc[-1] < sma50.iloc[-1]

            score = 0
            if df["close"].iloc[-1] > sma20.iloc[-1]: score += 1
            if rsi.iloc[-1] > 50: score += 1
            if macd.iloc[-1] > signal.iloc[-1]: score += 1
            if df["volume"].iloc[-1] > np.mean(df["volume"][-20:]): score += 1
            if cross_up: score += 2
            if cross_down: score -= 2

            # Generate the buy and sell signals
            cross_msg = ""
            if cross_up: cross_msg = f"{bcolors.OKGREEN}📈{bcolors.ENDC}"
            elif cross_down: cross_msg = f"{bcolors.FAIL}📉{bcolors.ENDC}"

            if score >= 4: signal_type = f"{bcolors.OKGREEN}🟢 Achat++{bcolors.ENDC}"
            elif score == 3: signal_type = f"{bcolors.OKGREEN}🟢 Achat+{bcolors.ENDC}"
            elif score == 2: signal_type = f"{bcolors.WARNING}🟡 Achat{bcolors.ENDC}"
            elif score <= -4: signal_type = f"{bcolors.FAIL}🔴 Vente++{bcolors.ENDC}"
            elif score == -3: signal_type = f"{bcolors.FAIL}🔴 Vente+{bcolors.ENDC}"
            elif score == -2: signal_type = f"{bcolors.WARNING}🟠 Vente{bcolors.ENDC}"
            else: signal_type = f"{bcolors.OKCYAN}🔵 Neutre{bcolors.ENDC}"

            print_signal_concise(i, j, score, signal_type, cross_msg)

        except Exception as e:
            print(f"{bcolors.FAIL}❌ {i} {j}: {e}{bcolors.ENDC}")
