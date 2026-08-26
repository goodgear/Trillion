from flask import Flask, jsonify
from armac.fetch import fetch
from armac.parser import parse
from engines import mag, port, web, index, pulse, swave, nstar
from core.aggregator import aggregate

app = Flask(__name__)

@app.get(from flask import Flask, jsonify
from armac.fetch import fetch_armac, fetch_yfinance
from armac.parser import parse_armac
from engines import mag, port, web, index, pulse, swave, nstar
from core.aggregator import aggregate

app = Flask(__name__)

@app.get("/run")
def run():
    # Try ARMAC first
    raw = fetch_armac()
    candles = parse_armac(raw) if raw else []

    # If ARMAC fails, fall back to yfinance
    if not candles:
        candles = fetch_yfinance("NVDA")

    engine_results = {
        "mag": mag.run(candles),
        "port": port.run(candles),
        "web": web.run(candles),
        "index": index.run(candles),
        "pulse": pulse.run(candles),
        "swave": swave.run(candles),
        "nstar": nstar.run(candles)
    }

    final = aggregate(candles, engine_results)
    return jsonify(final)

if __name__ == "__main__":
    app.run(debug=True)
)
def run():
    raw = fetch()
    candles = parse(raw)

    engine_results = {
        "mag": mag.run(candles),
        "port": port.run(candles),
        "web": web.run(candles),
        "index": index.run(candles),
        "pulse": pulse.run(candles),
        "swave": swave.run(candles),
        "nstar": nstar.run(candles)
    }

    final = aggregate(candles, engine_results)
    return jsonify(final)

if __name__ == "__main__":
    app.run(debug=True)
