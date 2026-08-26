def run(candles):
    # Index = trend confirmation
    signals = []
    for c in candles:
        signals.append("long")
    return signals
