from core.signal_map import ENGINE_MAP
from core.interference import resolve_interference
from core.dominance import dominant_engine

def aggregate(candles, engine_results):
    final = []
    for i in range(len(candles)):
        outputs = [engine_results[e][i] for e in engine_results]
        final.append({
            "signal": resolve_interference(outputs),
            "dominant": dominant_engine(outputs)
        })
    return final
