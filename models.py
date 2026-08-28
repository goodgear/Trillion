# models.py
from db import db
from datetime import datetime

# ---------------------------------------------------------
# USER MODEL
# ---------------------------------------------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email}>"

# ---------------------------------------------------------
# TICKER MODEL
# ---------------------------------------------------------
class Ticker(db.Model):
    __tablename__ = "tickers"

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(32), unique=True, nullable=False)

    def __repr__(self):
        return f"<Ticker {self.symbol}>"

# ---------------------------------------------------------
# SIGNAL MODEL
# ---------------------------------------------------------
class Signal(db.Model):
    __tablename__ = "signals"

    id = db.Column(db.Integer, primary_key=True)
    ticker_id = db.Column(db.Integer, db.ForeignKey("tickers.id"))
    time = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(16))          # BUY / SELL / HOLD / etc.
    confidence = db.Column(db.Float)         # 0.0–1.0

    ticker = db.relationship("Ticker")

    def __repr__(self):
        return f"<Signal {self.type} {self.confidence}>"

# ---------------------------------------------------------
# BACKTEST RESULTS
# ---------------------------------------------------------
class BacktestResult(db.Model):
    __tablename__ = "backtest_results"

    id = db.Column(db.Integer, primary_key=True)
    ticker_id = db.Column(db.Integer, db.ForeignKey("tickers.id"))
    range = db.Column(db.String(8))          # '1y', '2y'
    engines = db.Column(db.String(255))      # comma-separated engine names
    total_return = db.Column(db.Float)
    win_rate = db.Column(db.Float)
    equity_curve_json = db.Column(db.Text)   # serialized list of equity values
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    ticker = db.relationship("Ticker")

    def __repr__(self):
        return f"<Backtest {self.ticker_id} {self.total_return}%>"

# ---------------------------------------------------------
# CLOSING REPORT
# ---------------------------------------------------------
class ClosingReport(db.Model):
    __tablename__ = "closing_reports"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, unique=True)
    summary = db.Column(db.Text)
    success_rate = db.Column(db.Float)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f"<ClosingReport {self.date}>"

# ---------------------------------------------------------
# NEXT-DAY TODO ITEMS
# ---------------------------------------------------------
class TodoItem(db.Model):
    __tablename__ = "todo_items"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    ticker = db.Column(db.String(32))
    action = db.Column(db.Text)
    priority = db.Column(db.String(16))      # low / medium / high

    def __repr__(self):
        return f"<Todo {self.ticker} {self.priority}>"
