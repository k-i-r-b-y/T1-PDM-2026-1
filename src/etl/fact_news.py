from __future__ import annotations

from src.etl.cleaning import article_metrics


def build_fact_table(
    rows: list[dict[str, str]],
    date_key_by_date: dict[str, int],
    source_key_by_name: dict[str, int],
    region_key_by_name: dict[str, int],
) -> list[dict[str, object]]:
    """Create the fact table from cleaned rows and keyed dimensions."""
    facts: list[dict[str, object]] = []
    for row in rows:
        metrics = article_metrics(row)
        facts.append(
            {
                "article_id": row["article_id"],
                "title": row["title"],
                "body": row["body"],
                "publish_date": row["publish_date"],
                "date_key": date_key_by_date[row["publish_date"]],
                "source_key": source_key_by_name[row["source"]],
                "region_key": region_key_by_name[row["region"]],
                "country": row["country"],
                **metrics,
            }
        )
    return facts
