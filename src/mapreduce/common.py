from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Iterable, Iterator
from pathlib import Path

from src.etl.io import read_csv_rows
from src.utils.text import tokenize


MapPair = tuple[object, object]


def map_reduce(
    records: Iterable[dict[str, str]],
    mapper: Callable[[dict[str, str]], Iterable[MapPair]],
    reducer: Callable[[object, list[object]], object],
) -> Iterator[tuple[object, object]]:
    """Execute a manual single-machine MapReduce pass."""
    grouped: dict[object, list[object]] = defaultdict(list)
    for record in records:
        for key, value in mapper(record):
            grouped[key].append(value)

    for key in sorted(grouped):
        yield key, reducer(key, grouped[key])


def iter_fact_rows(warehouse_dir: Path) -> Iterator[dict[str, str]]:
    """Iterate all fact rows from partitioned CSV files."""
    for csv_path in sorted((warehouse_dir / "fact_news").glob("year=*/month=*/*.csv")):
        yield from read_csv_rows(csv_path, encoding="utf-8")


def document_tokens(record: dict[str, str], text_fields: tuple[str, ...] = ("title", "body")) -> list[str]:
    """Extract normalized tokens from selected fields."""
    tokens: list[str] = []
    for field in text_fields:
        tokens.extend(tokenize(record.get(field, "")))
    return tokens
