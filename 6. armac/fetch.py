import requests

def fetch():
    url = "http://localhost/timelapse/NVDA?tier=1h&ticker=NVDA"
    resp = requests.get(url)
    return resp.text
import requests
import yfinance as yf

# ARMAC local timelapse endpoint
ARMAC_URL = "http://localhost/timelapse/NVDA?tier=1h&ticker=NVDA"

def fetch_armac():
    """Fetch raw NVDA timelapse data from ARMAC."""
    try:
        resp = requests.get(ARMAC_URL)
        return resp.text
    except Exception as e:
        print("ARMAC fetch error:", e)
        return None

def fetch_yfinance(ticker="NVDA"):
    """Fetch NVDA candles from Yahoo Finance using yfinance."""
    try:
        data = yf.download(ticker, period="1d", interval="1h")
        candles = []

        for index, row in data.iterrows():
            candles.append({
                "time": str(index),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": float(row["Volume"])
            })

        return candles

    except Exception as e:
        print("yfinance fetch error:", e)
        return []
