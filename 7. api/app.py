from flask import Flask, jsonify
from engines.mag import mag_engine
from engines.port import port_engine
from engines.web import web_engine
from engines.index import index_engine
from engines.pulse import pulse_engine
from engines.swave import swave_engine
from engines.nstar import nstar_engine
from core.aggregator import aggregate_signals

app = Flask(__name__)

@app.get("/run")
def run_all():
    try:
        mag = mag_engine()
        port = port_engine()
        web = web_engine()
        index = index_engine()
        pulse = pulse_engine()
        swave = swave_engine()
        nstar = nstar_engine()

        result = aggregate_signals(
            mag=mag,
            port=port,
            web=web,
            index=index,
            pulse=pulse,
            swave=swave,
            nstar=nstar
        )

        return jsonify({
            "mag": mag,
            "port": port,
            "web": web,
            "index": index,
            "pulse": pulse,
            "swave": swave,
            "nstar": nstar,
            "aggregate": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
