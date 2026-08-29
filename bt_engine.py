# backtest.py
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import yfinance as yf

backtest_bp = Blueprint('backtest', __name__)

def simple_engine_strategy(prices):
    """
    Example engine logic:
    - Buy when close > previous close (up day)
    - Sell next day
    """
    trades = []
    position = None

    for i in range(1, len(prices)):
        today = prices[i]
        yesterday = prices[i - 1]

        # BUY signal: up day and no position
        if position is None and today["close"] > yesterday["close"]:
            position = {
                "entry_time": today["time"],
                "entry_price": today["close"]
            }

        # SELL next day if in position
        elif position is not None:
            trades.append({
                "entry_time": position["entry_time"],
                "entry_price": position["entry_price"],
                "exit_time": today["time"],
                "exit_price": today["close"],
            })
            position = None

    return trades

@backtest_bp.route('/backtest', methods=['POST'])
def backtest():
    data = request.get_json()
    ticker = data.get('ticker', 'AAPL')
    range_ = data.get('range', '2y')

    # -----------------------------
    # 1. Pull historical data
    # -----------------------------
    end = datetime.utcnow()
    if range_ == '1y':
        start = end - timedelta(days=365)
    else:
        start = end - timedelta(days=730)

    df = yf.download(ticker, start=start, end=end, interval="1d")

    if df.empty:
        return jsonify({"ok": False, "message": "Ticker not found"}), 404

    prices = []
    for idx, row in df.iterrows():
        prices.append({
            "time": idx.strftime("%Y-%m-%d"),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"])
        })

    # -----------------------------
    # 2. Run strategy (placeholder engine)
    # -----------------------------
    trades = simple_engine_strategy(prices)

    # -----------------------------
    # 3. Compute equity curve & stats
    # -----------------------------
    equity_curve = []
    equity = 10000.0  # starting capital
    wins = 0
    total_trades = len(trades)

    for t in trades:
        pnl = (t["exit_price"] - t["entry_price"])
        equity += pnl
        if pnl > 0:
            wins += 1

        equity_curve.append({
            "time": t["exit_time"],
            "equity": equity
        })

    total_return = ((equity - 10000.0) / 10000.0) * 100 if total_trades > 0 else 0.0
    win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0.0

    return jsonify({
        "ok": True,
        "ticker": ticker,
        "range": range_,
        "return": total_return,
        "win_rate": win_rate,
        "trades": trades,
        "equity_curve": equity_curve,
    })
