def run(candles):
    # N Star = compression engine
    signals = []
    for c in candles:
        signals.append("short")
    return signals
