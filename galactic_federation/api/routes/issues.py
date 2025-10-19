from __future__ import annotations
from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ..deps import DBDep, SettingsDep
from ...domain.services.issue_engine import IssueEngine

router = APIRouter(prefix='/issues', tags=['issues'])


class IssueResolutionRequest(BaseModel):
    planet_id: int
    issue_id: int
    option_id: int
    effects: dict[str, Any] = Field(default_factory=dict)


@router.get('')
def list_issues(db: DBDep, settings: SettingsDep):
    engine = IssueEngine(db=db, issues_per_day=settings.issues_per_day)
    return engine.available_issues()

@router.post('/resolve')
def resolve_issue(request: IssueResolutionRequest, db: DBDep, settings: SettingsDep):
    engine = IssueEngine(db=db, issues_per_day=settings.issues_per_day)
    try:
        new_state = engine.apply_decision(
            planet_id=request.planet_id,
            issue_id=request.issue_id,
            option_id=request.option_id,
            effects_payload=request.effects,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {'stats': new_state.stats, 'tags': sorted(new_state.tags)}
