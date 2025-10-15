from __future__ import annotations
from dataclasses import dataclass
from sqlalchemy.orm import Session
from ...infra.repos.planet_repo import PlanetRepo

@dataclass
class PlanetService:
    """High-level operations on planets (create, fetch)."""

    db: Session

    def create(self, name: str, slug: str):
        return PlanetRepo(self.db).create(name=name, slug=slug)

    def fetch(self, slug: str):
        return PlanetRepo(self.db).by_slug(slug)
