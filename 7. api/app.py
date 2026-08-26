from flask import Flask, jsonify
from armac.fetch import fetch
from armac.parser import parse
from engines import mag, port, web, index, pulse, swave, nstar
from core.aggregator import aggregate

app = Flask(__name__)

@app.get("/run")
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
