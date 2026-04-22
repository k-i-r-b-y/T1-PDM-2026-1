from __future__ import annotations

from collections import Counter


def compute_daily_counts(records: list[dict[str, str]]) -> dict[str, int]:
    """Count articles per publication day."""
    counts = Counter(record["publish_date"] for record in records)
    return dict(sorted(counts.items()))


def detect_daily_peaks(
    daily_counts: dict[str, int],
    window_size: int = 7,
    threshold_ratio: float = 1.5,
) -> list[dict[str, float]]:
    """Detect days whose volume exceeds a moving average threshold."""
    items = list(sorted(daily_counts.items()))
    peaks: list[dict[str, float]] = []

    for index, (date_value, count) in enumerate(items):
        start = max(0, index - window_size)
        history = [value for _, value in items[start:index]]
        if not history:
            continue
        moving_average = sum(history) / len(history)
        if moving_average and count >= moving_average * threshold_ratio:
            peaks.append(
                {
                    "publish_date": date_value,
                    "count": float(count),
                    "moving_average": moving_average,
                    "ratio": count / moving_average,
                }
            )

    return peaks
