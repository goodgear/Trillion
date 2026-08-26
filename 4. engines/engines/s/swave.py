def run(candles):
    # S-wave = volatility engine
    signals = []
    for c in candles:
        signals.append("long")
    return signals
