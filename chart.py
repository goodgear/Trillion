# chart.py
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import yfinance as yf

from db import db
from models import Signal, Ticker

chart_bp = Blueprint("chart", __name__)

# ---------------------------------------------------------
# Helper: Market status (open/closed)
# ---------------------------------------------------------
def get_market_status():
    now = datetime.utcnow()
    # NYSE hours: 13:30–20:00 UTC (9:30–4:00 EST)
    if 13 <= now.hour <= 20:
        return "open"
    return "closed"

# ---------------------------------------------------------
# Helper: Simple regime detection
# ---------------------------------------------------------
def detect_regimes(df):
    closes = df["Close"].tolist()
    regimes = []
    trend = None
    trend_start = None

    for i in range(1, len(closes)):
        today = closes[i]
        yesterday = closes[i - 1]

        if today > yesterday:
            new_trend = "uptrend"
        elif today < yesterday:
            new_trend = "downtrend"
        else:
            new_trend = "flat"

        if trend is None:
            trend = new_trend
            trend_start = df.index[i - 1]
        elif new_trend != trend:
            regimes.append({
                "start": trend_start.strftime("%Y-%m-%d"),
                "end": df.index[i - 1].strftime("%Y-%m-%d"),
                "label": trend
            })
            trend = new_trend
            trend_start = df.index[i]

    # Close last regime
    regimes.append({
        "start": trend_start.strftime("%Y-%m-%d"),
        "end": df.index[-1].strftime("%Y-%m-%d"),
        "label": trend
    })

    return regimes

# ---------------------------------------------------------
# Main chart endpoint
# ---------------------------------------------------------
@chart_bp.route("/chart_data")
def chart_data():
    ticker_symbol = request.args.get("ticker", "AAPL")

    # Ensure ticker exists in DB
    ticker_obj = Ticker.query.filter_by(symbol=ticker_symbol).first()
    if not ticker_obj:
        ticker_obj = Ticker(symbol=ticker_symbol)
        db.session.add(ticker_obj)
        db.session.commit()

    # -----------------------------------------------------
    # 1. Pull 2-year historical data
    # -----------------------------------------------------
    end = datetime.utcnow()
    start = end - timedelta(days=730)

    df = yf.download(ticker_symbol, start=start, end=end, interval="1d")
    if df.empty:
        return jsonify({"error": "Ticker not found"}), 404

    prices = []
    for idx, row in df.iterrows():
        prices.append({
            "time": idx.strftime("%Y-%m-%d"),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"])
        })

    # -----------------------------------------------------
    # 2. Stats
    # -----------------------------------------------------
    last_close = float(df["Close"].iloc[-1])
    prev_close = float(df["Close"].iloc[-2])
    change_pct = ((last_close - prev_close) / prev_close) * 100
    volume = int(df["Volume"].iloc[-1])
    market_status = get_market_status()

    # -----------------------------------------------------
    # 3. Signals from DB
    # -----------------------------------------------------
    db_signals = Signal.query.filter_by(ticker_id=ticker_obj.id).all()
    signals = [{
        "time": s.time.strftime("%Y-%m-%d %H:%M"),
        "type": s.type,
        "confidence": s.confidence
    } for s in db_signals]

    last_signal = signals[-1]["type"] if signals else None

    # -----------------------------------------------------
    # 4. Regimes
    # -----------------------------------------------------
    regimes = detect_regimes(df)

    # -----------------------------------------------------
    # 5. Confidence band (simple placeholder)
    # -----------------------------------------------------
    confidence_value = 0.65  # Replace with engine logic later
    confidence = [{
        "time": idx.strftime("%Y-%m-%d"),
        "value": confidence_value
    } for idx in df.index]

    # -----------------------------------------------------
    # 6. Final response
    # -----------------------------------------------------
    return jsonify({
        "prices": prices,
        "signals": signals,
        "regimes": regimes,
        "confidence": confidence,
        "stats": {
            "last_price": last_close,
            "change_pct": change_pct,
            "volume": volume,
            "market_status": market_status,
            "last_signal": last_signal,
            "consensus": "neutral",      # placeholder until engines added
            "confidence": confidence_value
        }
    })
