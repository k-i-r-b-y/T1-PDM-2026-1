from __future__ import annotations

from collections import Counter, defaultdict
import math

from src.mapreduce.common import document_tokens


def compute_source_divergence(records: list[dict[str, str]]) -> dict[str, float]:
    """Compute a smoothed divergence score per source against the global distribution."""
    source_counters: dict[str, Counter[str]] = defaultdict(Counter)
    global_counter: Counter[str] = Counter()

    for record in records:
        source = record.get("source_name") or record.get("source") or "unknown"
        tokens = document_tokens(record)
        source_counters[source].update(tokens)
        global_counter.update(tokens)

    total_global = sum(global_counter.values()) or 1
    vocabulary = set(global_counter)
    scores: dict[str, float] = {}

    for source, counter in sorted(source_counters.items()):
        total_source = sum(counter.values()) or 1
        divergence = 0.0
        for token in vocabulary:
            p = (counter[token] + 1) / (total_source + len(vocabulary))
            q = (global_counter[token] + 1) / (total_global + len(vocabulary))
            divergence += p * math.log(p / q)
        scores[source] = divergence

    return scores
