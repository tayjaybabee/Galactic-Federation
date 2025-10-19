from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..schemas import Issue, IssueOption

class IssueRepo:
    def __init__(self, db: Session):
        self._db = db

    def active(self) -> list[Issue]:
        return list(self._db.scalars(select(Issue).where(Issue.active.is_(True))).all())

    def options_for(self, issue_id: int) -> list[IssueOption]:
        return list(self._db.scalars(select(IssueOption).where(IssueOption.issue_id == issue_id)).all())
