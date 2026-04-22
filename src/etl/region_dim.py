from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import re

from src.etl.config import UNKNOWN_REGION
from src.utils.text import canonicalize_text


REGION_ALIASES: dict[str, tuple[str, ...]] = {
    "Arica y Parinacota": ("arica", "parinacota"),
    "Tarapacá": ("tarapaca", "iquique"),
    "Antofagasta": ("antofagasta", "calama", "tocopilla"),
    "Atacama": ("atacama", "copiapo", "vallenar"),
    "Coquimbo": ("coquimbo", "la serena", "ovalle"),
    "Valparaíso": ("valparaiso", "vina del mar", "quilpue"),
    "Metropolitana": ("metropolitana", "santiago", "rm", "region metropolitana", "capital"),
    "O'Higgins": ("ohiggins", "rancagua", "san fernando"),
    "Maule": ("maule", "talca", "curico", "linares"),
    "Ñuble": ("nuble", "chillan"),
    "Biobío": ("biobio", "concepcion", "los angeles", "talcahuano"),
    "La Araucanía": ("araucania", "temuco", "villarrica"),
    "Los Ríos": ("los rios", "valdivia"),
    "Los Lagos": ("los lagos", "puerto montt", "osorno", "chiloe"),
    "Aysén": ("aysen", "coyhaique"),
    "Magallanes": ("magallanes", "punta arenas"),
    UNKNOWN_REGION: ("desconocida",),
}


@dataclass(frozen=True)
class RegionMatch:
    """Weighted region match extracted from an article."""

    region_name: str
    score: int


def build_region_dimension() -> list[dict[str, object]]:
    """Create the region dimension including the fallback category."""
    regions = list(REGION_ALIASES.keys())
    return [
        {
            "region_key": index,
            "region_name": region_name,
        }
        for index, region_name in enumerate(regions, start=1)
    ]


def infer_region(title: str, body: str, title_weight: int = 3, body_weight: int = 1) -> str:
    """Infer a region using accent-insensitive alias matching."""
    title_text = canonicalize_text(title)
    body_text = canonicalize_text(body)
    scores: Counter[str] = Counter()

    for region_name, aliases in REGION_ALIASES.items():
        if region_name == UNKNOWN_REGION:
            continue
        for alias in aliases:
            pattern = rf"(?<!\w){re.escape(alias)}(?!\w)"
            title_matches = len(re.findall(pattern, title_text))
            body_matches = len(re.findall(pattern, body_text))
            if title_matches:
                scores[region_name] += title_matches * title_weight
            if body_matches:
                scores[region_name] += body_matches * body_weight

    if not scores:
        return UNKNOWN_REGION

    highest_score = max(scores.values())
    candidates = sorted(region for region, score in scores.items() if score == highest_score)
    return candidates[0]
