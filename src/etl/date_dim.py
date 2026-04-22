from __future__ import annotations

from datetime import datetime


def build_date_record(date_value: str) -> dict[str, object]:
    """Build a date dimension record from an ISO date."""
    parsed = datetime.strptime(date_value, "%Y-%m-%d").date()
    return {
        "date_key": int(parsed.strftime("%Y%m%d")),
        "full_date": parsed.isoformat(),
        "year": parsed.year,
        "month": parsed.month,
        "day": parsed.day,
        "day_of_week": parsed.weekday(),
        "day_name": parsed.strftime("%A"),
    }


def build_date_dimension(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    """Create distinct date dimension rows."""
    unique_dates = sorted({row["publish_date"] for row in rows})
    return [build_date_record(date_value) for date_value in unique_dates]
