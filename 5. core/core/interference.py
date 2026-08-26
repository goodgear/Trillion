def resolve_interference(engine_outputs):
    # Simple majority vote
    counts = {"long":0, "short":0, "flat":0}
    for sig in engine_outputs:
        counts[sig] += 1
    return max(counts, key=counts.get)
