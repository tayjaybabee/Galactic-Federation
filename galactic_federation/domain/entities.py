from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class PlanetState:
    """In-memory state representation for effects application.

    Properties:
        stats: Nested dict of stat categories → { 'value': float }.
        tags: Set of string tags applied to the planet.
    """

    stats: dict[str, dict[str, float]] = field(default_factory=lambda: {
        'economy': {'value': 0.5},
        'civil_rights': {'value': 0.5},
        'political_freedom': {'value': 0.5},
    })
    tags: set[str] = field(default_factory=set)
