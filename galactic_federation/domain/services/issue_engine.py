from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from ...infra.repos.issue_repo import IssueRepo
from ..entities import PlanetState

# Utilities

def _resolve_path(state: dict, path: str) -> tuple[dict, str]:
    """Resolve dotted path to a parent node and key; create nodes as needed."""
    parts = path.split('.')
    node = state
    for key in parts[:-1]:
        if key not in node or not isinstance(node[key], dict):
            node[key] = {}
        node = node[key]
    return node, parts[-1]

@dataclass
class DecisionResolver:
    """Apply a list of effects to a planet state.

    Notes:
        Effects are data-driven:
        {
          "effects": [
            {"op": "add", "path": "economy.value", "value": 0.1},
            {"op": "mul", "path": "civil_rights.value", "value": 0.95},
            {"op": "tag", "path": "tags", "value": "surveillance_state"}
          ]
        }
    """

    def apply_all(self, state: PlanetState, payload: dict[str, Any]) -> PlanetState:
        for eff in payload.get('effects', []):
            op = eff['op']
            path = eff['path']
            val = eff['value']
            if op == 'add':
                node, key = _resolve_path(state.stats, path)
                node[key] = float(node.get(key, 0.0)) + float(val)
            elif op == 'mul':
                node, key = _resolve_path(state.stats, path)
                node[key] = float(node.get(key, 0.0)) * float(val)
            elif op == 'tag':
                state.tags.add(str(val))
        # clamp core values 0..1 for MVP
        for k in ('economy', 'civil_rights', 'political_freedom'):
            v = state.stats.get(k, {}).get('value', 0.5)
            state.stats[k]['value'] = max(0.0, min(1.0, float(v)))
        return state

@dataclass
class IssueEngine:
    """Select issues and resolve decisions for a given planet.

    Parameters:
        db: Active SQLAlchemy session.
        issues_per_day: Count of issues surfaced daily.
    """

    db: Any
    issues_per_day: int

    def available_issues(self) -> list[dict]:
        repo = IssueRepo(self.db)
        return [
            {
                'id': i.id,
                'title': i.title,
                'prompt': i.prompt,
                'tags': i.tags,
            }
            for i in repo.active()
        ]

    def apply_decision(self, planet_state: PlanetState, effects_payload: dict) -> PlanetState:
        return DecisionResolver().apply_all(planet_state, effects_payload)
