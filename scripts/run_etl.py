from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.etl.cleaning import clean_raw_row
from src.etl.config import EtlSettings, build_project_paths
from src.etl.date_dim import build_date_dimension
from src.etl.fact_news import build_fact_table
from src.etl.io import read_csv_rows, write_csv_rows
from src.etl.partitioning import write_partitioned_fact_table
from src.etl.region_dim import build_region_dimension, infer_region
from src.etl.source_dim import build_source_dimension
from src.etl.validation import (
    validate_fact_row_count,
    validate_non_empty_identifiers,
    validate_partition_keys,
    validate_referential_integrity,
    validate_unique_dimension_keys,
)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the ETL pipeline."""
    parser = argparse.ArgumentParser(description="Build the warehouse from the raw news CSV.")
    parser.add_argument("--limit", type=int, default=None, help="Optional row limit for smoke runs.")
    return parser.parse_args()


def run_etl(limit: int | None = None) -> None:
    """Execute the base ETL flow end to end."""
    paths = build_project_paths(ROOT_DIR)
    settings = EtlSettings()

    raw_rows = list(read_csv_rows(paths.raw_news_path, encoding=settings.csv_encoding))
    if limit is not None:
        raw_rows = raw_rows[:limit]

    cleaned_rows = [clean_raw_row(row) for row in raw_rows]
    validate_non_empty_identifiers(cleaned_rows)

    for row in cleaned_rows:
        row["region"] = infer_region(
            title=row["title"],
            body=row["body"],
            title_weight=settings.region_priority_title_weight,
            body_weight=settings.region_priority_body_weight,
        )

    dim_date = build_date_dimension(cleaned_rows)
    dim_source = build_source_dimension(cleaned_rows)
    dim_region = build_region_dimension()

    date_key_by_date = {row["full_date"]: row["date_key"] for row in dim_date}
    source_key_by_name = {row["source_name"]: row["source_key"] for row in dim_source}
    region_key_by_name = {row["region_name"]: row["region_key"] for row in dim_region}

    fact_rows = build_fact_table(
        rows=cleaned_rows,
        date_key_by_date=date_key_by_date,
        source_key_by_name=source_key_by_name,
        region_key_by_name=region_key_by_name,
    )

    validate_unique_dimension_keys(dim_date, "date_key")
    validate_unique_dimension_keys(dim_source, "source_key")
    validate_unique_dimension_keys(dim_region, "region_key")
    validate_fact_row_count(raw_count=len(raw_rows), fact_count=len(fact_rows))
    validate_partition_keys(fact_rows)
    validate_referential_integrity(
        fact_rows=fact_rows,
        valid_date_keys=set(date_key_by_date.values()),
        valid_source_keys=set(source_key_by_name.values()),
        valid_region_keys=set(region_key_by_name.values()),
    )

    write_csv_rows(
        paths.warehouse_dir / "dim_date" / "dim_date.csv",
        fieldnames=list(dim_date[0].keys()),
        rows=dim_date,
    )
    write_csv_rows(
        paths.warehouse_dir / "dim_source" / "dim_source.csv",
        fieldnames=list(dim_source[0].keys()),
        rows=dim_source,
    )
    write_csv_rows(
        paths.warehouse_dir / "dim_region" / "dim_region.csv",
        fieldnames=list(dim_region[0].keys()),
        rows=dim_region,
    )
    write_partitioned_fact_table(
        warehouse_dir=paths.warehouse_dir,
        rows=fact_rows,
        filename=settings.fact_filename,
    )


if __name__ == "__main__":
    args = parse_args()
    run_etl(limit=args.limit)
