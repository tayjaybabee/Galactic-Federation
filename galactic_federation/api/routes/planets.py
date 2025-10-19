from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, constr, field_validator
from ..deps import DBDep
from ...domain.services.planet_service import PlanetService

router = APIRouter(prefix='/planets', tags=['planets'])

class PlanetCreateRequest(BaseModel):
    name: constr(min_length=1, max_length=100)
    slug: constr(min_length=1, max_length=50, pattern=r'^[a-z0-9-]+$')

    @field_validator('name')
    @classmethod
    def name_must_have_content(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('name must contain non-whitespace characters')
        return value


@router.post('')
def create_planet(request: PlanetCreateRequest, db: DBDep):
    svc = PlanetService(db)
    normalized_slug = request.slug.lower()
    if svc.fetch(normalized_slug):
        raise HTTPException(status_code=400, detail='planet with this slug already exists')
    planet = svc.create(name=request.name.strip(), slug=normalized_slug)
    return {
        'id': planet.id,
        'name': planet.name,
        'slug': planet.slug,
        'stats': planet.stats,
    }

@router.get('/{slug}')
def get_planet(slug: str, db: DBDep):
    if planet := PlanetService(db).fetch(slug):
        return {
            'id': planet.id,
            'name': planet.name,
            'slug': planet.slug,
            'stats': planet.stats,
        }
    raise HTTPException(status_code=404, detail='planet not found')
