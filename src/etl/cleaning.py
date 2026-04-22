from __future__ import annotations

from src.utils.text import normalize_text


EXPECTED_COLUMNS = (
    "article_id",
    "title",
    "body",
    "publish_date",
    "source",
    "country",
)


def clean_raw_row(row: dict[str, str]) -> dict[str, str]:
    """Normalize a raw news row while preserving source data."""
    return {
        "article_id": normalize_text(row.get("article_id", "")),
        "title": normalize_text(row.get("title", "")),
        "body": normalize_text(row.get("body", "")),
        "publish_date": normalize_text(row.get("publish_date", "")),
        "source": normalize_text(row.get("source", "")).lower(),
        "country": normalize_text(row.get("country", "")),
    }


def article_metrics(row: dict[str, str]) -> dict[str, int]:
    """Compute lightweight derived metrics for the fact table."""
    title_tokens = row["title"].split()
    body_tokens = row["body"].split()
    return {
        "title_word_count": len(title_tokens),
        "body_word_count": len(body_tokens),
        "title_char_count": len(row["title"]),
        "body_char_count": len(row["body"]),
    }
