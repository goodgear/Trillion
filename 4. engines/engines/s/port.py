def run(candles):
    # Port = pullback engine
    signals = []
    for c in candles:
        signals.append("short")
    return signals
