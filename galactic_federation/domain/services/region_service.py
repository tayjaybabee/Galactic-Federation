from __future__ import annotations
from dataclasses import dataclass
from sqlalchemy.orm import Session
from ...infra.repos.region_repo import SectorRepo

@dataclass
class RegionService:
    db: Session

    def fetch(self, slug: str):
        return SectorRepo(self.db).by_slug(slug)
