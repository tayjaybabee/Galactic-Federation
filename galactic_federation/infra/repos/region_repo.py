from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..schemas import Sector

class SectorRepo:
    def __init__(self, db: Session):
        self._db = db

    def by_slug(self, slug: str) -> Sector | None:
        return self._db.scalars(select(Sector).where(Sector.slug == slug)).first()
