import requests
from flask import Blueprint, jsonify

scan_bp = Blueprint("scan", __name__)

# Your ARMAC endpoint base URL
ARMAC_URL = "http://localhost/signals"

def get_armac_signal(ticker: str, tier: str = "5m"):
    """Fetch ARMAC signal for a ticker."""
    try:
        url = f"{ARMAC_URL}?ticker={ticker}&tier={tier}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@scan_bp.route("/scan/<ticker>", methods=["GET"])
def scan_ticker(ticker):
    """Run a repeatability scan using ARMAC signals."""
    # 1. Pull ARMAC signal
    armac = get_armac_signal(ticker)

    if "error" in armac:
        return jsonify({"ticker": ticker, "error": armac["error"]}), 500

    # 2. Extract key ARMAC fields
    signal = armac.get("signal")
    confidence = armac.get("confidence")
    trap_pressure = armac.get("trap_pressure_index")
    failure_point = armac.get("failure_point_index")

    # 3. Build your repeatability test result
    result = {
        "ticker": ticker,
        "signal": signal,
        "confidence": confidence,
        "trap_pressure_index": trap_pressure,
        "failure_point_index": failure_point,
        "status": "ARMAC-integrated scan complete"
    }

    return jsonify(result), 200
