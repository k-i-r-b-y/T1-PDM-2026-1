from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Iterator


def read_csv_rows(path: Path, encoding: str = "utf-8-sig") -> Iterator[dict[str, str]]:
    """Yield rows from a CSV file as dictionaries."""
    with path.open("r", encoding=encoding, newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            yield dict(row)


def write_csv_rows(
    path: Path,
    fieldnames: list[str],
    rows: Iterable[dict[str, object]],
    encoding: str = "utf-8",
) -> None:
    """Write dictionaries to a CSV file with a fixed schema."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding=encoding, newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
