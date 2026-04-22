from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.etl.config import build_project_paths
from src.mapreduce.common import iter_fact_rows
from src.mapreduce.daily_peaks import compute_daily_counts, detect_daily_peaks
from src.mapreduce.region_word_distribution import compute_region_word_distribution
from src.mapreduce.source_divergence import compute_source_divergence
from src.mapreduce.top_k_terms import compute_top_k_terms_by_month


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for analytics execution."""
    parser = argparse.ArgumentParser(description="Run base MapReduce analytics on the warehouse.")
    parser.add_argument(
        "--analysis",
        choices=("top_k_terms", "region_word_distribution", "source_divergence", "daily_peaks"),
        required=True,
        help="Analysis to execute.",
    )
    parser.add_argument("--limit", type=int, default=None, help="Optional row limit for smoke runs.")
    return parser.parse_args()


def run_analysis(name: str, limit: int | None = None) -> object:
    """Dispatch a selected analysis over fact rows."""
    paths = build_project_paths(ROOT_DIR)
    records = list(iter_fact_rows(paths.warehouse_dir))
    if limit is not None:
        records = records[:limit]

    if name == "top_k_terms":
        return compute_top_k_terms_by_month(records)
    if name == "region_word_distribution":
        return compute_region_word_distribution(records)
    if name == "source_divergence":
        return compute_source_divergence(records)
    if name == "daily_peaks":
        daily_counts = compute_daily_counts(records)
        return detect_daily_peaks(daily_counts)
    raise ValueError(f"analisis no soportado: {name}")


if __name__ == "__main__":
    args = parse_args()
    result = run_analysis(name=args.analysis, limit=args.limit)
    print(json.dumps(result, indent=2, ensure_ascii=False))
