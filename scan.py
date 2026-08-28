import datetime as dt
import requests
from flask import Blueprint, jsonify, request

scan_bp = Blueprint("scan", __name__)

ARMAC_URL = "http://localhost/signals"


def get_armac_signal(ticker: str, tier: str = "5m"):
    """Fetch ARMAC signal for a ticker."""
    try:
        url = f"{ARMAC_URL}?ticker={ticker}&tier={tier}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def in_ny_session(ts: dt.datetime) -> bool:
    """Check if timestamp is inside NY session (approx 9:30–16:00 ET)."""
    # assuming ts is already in ET or naive market time
    return 9 <= ts.hour <= 16


def compute_bos_choch(structure_points):
    """
    Very simplified BOS/CHOCH read:
    structure_points: list of dicts with { 'time', 'high', 'low' }
    """
    if len(structure_points) < 3:
        return {"bos": None, "choch": None}

    # naive: last leg direction
    last = structure_points[-1]
    prev = structure_points[-2]

    direction = "bullish" if last["high"] > prev["high"] else "bearish"

    bos = {
        "type": direction,
        "ref_high": last["high"],
        "ref_low": last["low"],
        "time": last["time"],
    }

    # CHOCH: simple opposite break of previous swing
    choch = None
    if direction == "bullish" and last["low"] < prev["low"]:
        choch = {
            "type": "bearish",
            "ref_low": last["low"],
            "time": last["time"],
        }
    elif direction == "bearish" and last["high"] > prev["high"]:
        choch = {
            "type": "bullish",
            "ref_high": last["high"],
            "time": last["time"],
        }

    return {"bos": bos, "choch": choch}


def find_fvg(candles):
    """
    Simplified FVG: look for 3-candle imbalance.
    candles: list of dicts with { 'time', 'high', 'low' }
    """
    if len(candles) < 3:
        return None

    fvg_list = []
    for i in range(2, len(candles)):
        c0 = candles[i - 2]
        c1 = candles[i - 1]
        c2 = candles[i]

        # bullish FVG: c0.high < c2.low (gap)
        if c0["high"] < c2["low"]:
            fvg_list.append({
                "type": "bullish",
                "start": c0["high"],
                "end": c2["low"],
                "time": c1["time"],
            })
        # bearish FVG: c0.low > c2.high
        if c0["low"] > c2["high"]:
            fvg_list.append({
                "type": "bearish",
                "start": c2["high"],
                "end": c0["low"],
                "time": c1["time"],
            })

    return fvg_list[-1] if fvg_list else None


def risk_reward(entry: float, stop: float, target_r_multiple: float = 3.0):
    """
    Compute 3R target given entry and stop.
    """
    if entry is None or stop is None:
        return None

    risk = abs(entry - stop)
    if risk == 0:
        return None

    if entry > stop:
        target = entry + risk * target_r_multiple
        side = "long"
    else:
        target = entry - risk * target_r_multiple
        side = "short"

    return {
        "side": side,
        "entry": entry,
        "stop": stop,
        "target": target,
        "r_multiple": target_r_multiple,
    }


@scan_bp.route("/scan/<ticker>", methods=["GET"])
def scan_ticker(ticker):
    """
    Full repeatability scan:
    - Pull ARMAC signal
    - Read basic BOS/CHOCH from structure
    - Find last FVG
    - Enforce NY session entry
    - Compute 3R target
    """
    tier = request.args.get("tier", "5m")

    armac = get_armac_signal(ticker, tier=tier)
    if "error" in armac:
        return jsonify({"ticker": ticker, "error": armac["error"]}), 500

    # Expect ARMAC to provide some structure/candle data
    candles = armac.get("candles", [])
    structure_points = [
        {
            "time": dt.datetime.fromisoformat(c["time"]),
            "high": c["high"],
            "low": c["low"],
        }
        for c in candles
    ]

    ms = compute_bos_choch(structure_points)
    fvg = find_fvg(structure_points)

    # NY session filter: use last candle time
    ny_ok = False
    if structure_points:
        ny_ok = in_ny_session(structure_points[-1]["time"])

    # crude entry/stop from FVG + BOS direction
    rr = None
    if fvg and ms["bos"]:
        if ms["bos"]["type"] == "bullish" and fvg["type"] == "bullish":
            entry = fvg["start"]
            stop = ms["bos"]["ref_low"]
            rr = risk_reward(entry, stop, target_r_multiple=3.0)
        elif ms["bos"]["type"] == "bearish" and fvg["type"] == "bearish":
            entry = fvg["start"]
            stop = ms["bos"]["ref_high"]
            rr = risk_reward(entry, stop, target_r_multiple=3.0)

    result = {
        "ticker": ticker,
        "tier": tier,
        "armac_signal": {
            "raw": armac,
            "confidence": armac.get("confidence"),
            "signal": armac.get("signal"),
        },
        "market_structure": {
            "bos": ms["bos"],
            "choch": ms["choch"],
        },
        "fvg": fvg,
        "ny_session_ok": ny_ok,
        "risk_reward_3R": rr,
        "status": "scan_complete",
    }

    return jsonify(result), 200

