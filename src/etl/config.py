from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


RAW_FILENAME = "noticias_chile_2023_2025_unique_article_id.csv"
UNKNOWN_REGION = "Desconocida"


@dataclass(frozen=True)
class ProjectPaths:
    """Centralized project paths for ETL and analytics."""

    root_dir: Path
    data_dir: Path = field(init=False)
    raw_dir: Path = field(init=False)
    warehouse_dir: Path = field(init=False)
    analytics_dir: Path = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "data_dir", self.root_dir / "data")
        object.__setattr__(self, "raw_dir", self.data_dir / "raw")
        object.__setattr__(self, "warehouse_dir", self.data_dir / "warehouse")
        object.__setattr__(self, "analytics_dir", self.data_dir / "analytics")

    @property
    def raw_news_path(self) -> Path:
        """Return the canonical raw input file."""
        return self.raw_dir / RAW_FILENAME


@dataclass(frozen=True)
class EtlSettings:
    """Runtime settings for the ETL pipeline."""

    unknown_region: str = UNKNOWN_REGION
    region_priority_title_weight: int = 3
    region_priority_body_weight: int = 1
    csv_encoding: str = "utf-8-sig"
    fact_filename: str = "part-00000.csv"


def build_project_paths(root_dir: Path) -> ProjectPaths:
    """Build path configuration from repository root."""
    return ProjectPaths(root_dir=root_dir)
