from __future__ import annotations

from collections import Counter

from src.mapreduce.common import document_tokens


DEFAULT_STOPWORDS = {
    "de", "la", "el", "en", "y", "a", "los", "las", "del", "por", "para", "con", "un", "una",
}


def compute_top_k_terms_by_month(
    records: list[dict[str, str]],
    k: int = 20,
    stopwords: set[str] | None = None,
) -> dict[str, list[tuple[str, int]]]:
    """Compute monthly top-k term frequencies on fact rows."""
    stopwords = stopwords or DEFAULT_STOPWORDS
    buckets: dict[str, Counter[str]] = {}

    for record in records:
        month_key = record["publish_date"][:7]
        counter = buckets.setdefault(month_key, Counter())
        for token in document_tokens(record):
            if token not in stopwords:
                counter[token] += 1

    return {
        month_key: counter.most_common(k)
        for month_key, counter in sorted(buckets.items())
    }


def main(records: list[dict[str, str]]) -> dict[str, list[tuple[str, int]]]:
    """Entry point placeholder for the monthly top-k analysis."""
    return compute_top_k_terms_by_month(records)
