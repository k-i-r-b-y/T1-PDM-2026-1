from __future__ import annotations


def build_source_dimension(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    """Create a surrogate-keyed source dimension."""
    sources = sorted({row["source"] for row in rows})
    return [
        {
            "source_key": index,
            "source_name": source,
        }
        for index, source in enumerate(sources, start=1)
    ]
