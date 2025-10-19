from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from ...infra.repos.issue_repo import IssueRepo
from ...infra.repos.planet_repo import PlanetRepo
from ...infra.schemas import Decision
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
            else:
                raise ValueError(f"unsupported effect operation '{op}'")
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

    db: Session
    issues_per_day: int

    def available_issues(self) -> list[dict]:
        repo = IssueRepo(self.db)
        issues = repo.active()[: self.issues_per_day]
        return [
            {
                'id': issue.id,
                'title': issue.title,
                'prompt': issue.prompt,
                'tags': issue.tags,
                'options': [
                    {
                        'id': option.id,
                        'text': option.text,
                        'effects': option.effects_json,
                    }
                    for option in repo.options_for(issue.id)
                ],
            }
            for issue in issues
        ]

    def apply_decision(
        self,
        *,
        planet_id: int,
        issue_id: int,
        option_id: int,
        effects_payload: dict[str, Any] | None,
    ) -> PlanetState:
        repo = PlanetRepo(self.db)
        planet = repo.by_id(planet_id)
        if planet is None:
            raise LookupError(f'planet {planet_id} not found')

        state = PlanetState()
        existing_stats = planet.stats if isinstance(planet.stats, dict) else {}
        for key, value in existing_stats.items():
            if key == 'tags':
                if isinstance(value, list):
                    state.tags.update(str(tag) for tag in value)
                continue
            if isinstance(value, dict):
                state.stats.setdefault(key, {})
                state.stats[key].update(value)

        payload = effects_payload or {}
        new_state = DecisionResolver().apply_all(state, payload)

        updated_stats = {k: dict(v) for k, v in new_state.stats.items()}
        if new_state.tags:
            updated_stats['tags'] = sorted(new_state.tags)
        else:
            updated_stats.pop('tags', None)
        planet.stats = updated_stats

        decision = Decision(
            planet_id=planet_id,
            issue_id=issue_id,
            option_id=option_id,
            effects_applied_json=payload,
        )
        self.db.add(decision)
        self.db.commit()
        self.db.refresh(planet)
        return new_state
