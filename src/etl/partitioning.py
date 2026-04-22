from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from src.etl.io import write_csv_rows


def partition_fact_rows(rows: list[dict[str, object]]) -> dict[tuple[str, str], list[dict[str, object]]]:
    """Group fact rows by year and month."""
    partitions: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        publish_date = str(row["publish_date"])
        year, month, _ = publish_date.split("-")
        partitions[(year, month)].append(row)
    return dict(partitions)


def write_partitioned_fact_table(
    warehouse_dir: Path,
    rows: list[dict[str, object]],
    filename: str,
) -> list[Path]:
    """Persist fact rows under year/month partitions."""
    fieldnames = list(rows[0].keys()) if rows else []
    written_paths: list[Path] = []

    for (year, month), partition_rows in sorted(partition_fact_rows(rows).items()):
        path = warehouse_dir / "fact_news" / f"year={year}" / f"month={month}" / filename
        write_csv_rows(path=path, fieldnames=fieldnames, rows=partition_rows)
        written_paths.append(path)

    return written_paths
