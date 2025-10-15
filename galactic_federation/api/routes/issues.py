from __future__ import annotations
from fastapi import APIRouter
from ..deps import DBDep, SettingsDep
from ...domain.entities import PlanetState
from ...domain.services.issue_engine import IssueEngine

router = APIRouter(prefix='/issues', tags=['issues'])

@router.get('')
def list_issues(db: DBDep, settings: SettingsDep):
    engine = IssueEngine(db=db, issues_per_day=settings.issues_per_day)
    return engine.available_issues()

@router.post('/resolve')
def resolve_issue(effects: dict, db: DBDep, settings: SettingsDep):
    state = PlanetState()
    engine = IssueEngine(db=db, issues_per_day=settings.issues_per_day)
    new_state = engine.apply_decision(state, effects)
    return {'stats': new_state.stats, 'tags': sorted(new_state.tags)}
