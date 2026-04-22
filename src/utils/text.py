from __future__ import annotations

import re
import unicodedata
from collections import Counter

TOKEN_PATTERN = re.compile(r"[a-z0-9áéíóúüñ]+", re.IGNORECASE)


def normalize_text(value: str) -> str:
    """Normalize whitespace and preserve content semantics."""
    collapsed = " ".join((value or "").split())
    return collapsed.strip()


def strip_accents(value: str) -> str:
    """Remove diacritics for accent-insensitive matching."""
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def canonicalize_text(value: str) -> str:
    """Lowercase and remove accents for matching operations."""
    return strip_accents(value).lower().strip()


def tokenize(value: str) -> list[str]:
    """Split text into normalized lexical tokens."""
    return [token.lower() for token in TOKEN_PATTERN.findall(value or "")]


def token_counts(value: str) -> Counter[str]:
    """Count tokens in a text field."""
    return Counter(tokenize(value))
