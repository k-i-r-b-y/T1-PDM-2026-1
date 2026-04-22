from __future__ import annotations

from collections import Counter, defaultdict


def compute_region_word_distribution(
    records: list[dict[str, str]],
    min_global_frequency: int = 5,
) -> list[dict[str, float | str]]:
    """Compute a base structure for regional vs global term frequencies."""
    regional_counts: dict[tuple[str, str], int] = defaultdict(int)
    global_counts: Counter[str] = Counter()

    for record in records:
        region = record.get("region_name") or record.get("region") or "Desconocida"
        for token in (record.get("body", "") + " " + record.get("title", "")).lower().split():
            global_counts[token] += 1
            regional_counts[(region, token)] += 1

    results: list[dict[str, float | str]] = []
    for (region, token), regional_count in sorted(regional_counts.items()):
        global_count = global_counts[token]
        if global_count < min_global_frequency:
            continue
        results.append(
            {
                "region": region,
                "term": token,
                "regional_count": float(regional_count),
                "global_count": float(global_count),
                "relative_ratio": regional_count / global_count,
            }
        )
    return results
