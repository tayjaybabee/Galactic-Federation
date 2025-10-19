from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from ..schemas import Planet

class PlanetRepo:
    """Repository for Planet persistence operations."""

    def __init__(self, db: Session):
        self._db = db

    def by_slug(self, slug: str) -> Planet | None:
        return self._db.scalars(
            select(Planet).where(func.lower(Planet.slug) == slug.lower())
        ).first()

    def by_id(self, planet_id: int) -> Planet | None:
        return self._db.get(Planet, planet_id)

    def create(self, name: str, slug: str) -> Planet:
        planet = Planet(name=name, slug=slug.lower(), stats={
            'economy': {'value': 0.5},
            'civil_rights': {'value': 0.5},
            'political_freedom': {'value': 0.5},
        })
        self._db.add(planet)
        self._db.commit()
        self._db.refresh(planet)
        return planet
