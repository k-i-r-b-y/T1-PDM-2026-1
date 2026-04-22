from __future__ import annotations

from collections import Counter


def validate_referential_integrity(
    fact_rows: list[dict[str, object]],
    valid_date_keys: set[int],
    valid_source_keys: set[int],
    valid_region_keys: set[int],
) -> None:
    """Ensure all fact foreign keys point to existing dimension keys."""
    for row in fact_rows:
        if row["date_key"] not in valid_date_keys:
            raise ValueError(f"date_key invalida: {row['date_key']}")
        if row["source_key"] not in valid_source_keys:
            raise ValueError(f"source_key invalida: {row['source_key']}")
        if row["region_key"] not in valid_region_keys:
            raise ValueError(f"region_key invalida: {row['region_key']}")


def validate_fact_row_count(raw_count: int, fact_count: int) -> None:
    """Ensure the fact table preserves the raw row count."""
    if raw_count != fact_count:
        raise ValueError(f"conteo inconsistente: raw={raw_count}, fact={fact_count}")


def validate_unique_dimension_keys(rows: list[dict[str, object]], key_name: str) -> None:
    """Ensure dimension surrogate keys are unique."""
    counts = Counter(row[key_name] for row in rows)
    duplicates = [value for value, count in counts.items() if count > 1]
    if duplicates:
        raise ValueError(f"llaves duplicadas en {key_name}: {duplicates}")


def validate_partition_keys(rows: list[dict[str, object]]) -> None:
    """Ensure partitionable dates follow the expected ISO structure."""
    for row in rows:
        publish_date = str(row["publish_date"])
        parts = publish_date.split("-")
        if len(parts) != 3 or any(not part for part in parts):
            raise ValueError(f"publish_date invalida para particion: {publish_date}")


def validate_non_empty_identifiers(rows: list[dict[str, str]]) -> None:
    """Ensure critical identifiers are available after cleaning."""
    for row in rows:
        if not row["article_id"]:
            raise ValueError("article_id vacio")
        if not row["publish_date"]:
            raise ValueError("publish_date vacia")
        if not row["source"]:
            raise ValueError("source vacio")
