def dominant_engine(engine_outputs):
    # Returns the engine with the strongest signal presence
    from collections import Counter
    return Counter(engine_outputs).most_common(1)[0][0]
