from __future__ import annotations
from .settings import get_settings

def is_enabled(flag: str) -> bool:
    """Return True if a given feature flag is enabled."""
    return flag in get_settings().flags
