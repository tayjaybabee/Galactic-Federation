from __future__ import annotations
from fastapi import APIRouter, HTTPException
from ..deps import DBDep
from ...domain.services.planet_service import PlanetService

router = APIRouter(prefix='/planets', tags=['planets'])

@router.post('')
def create_planet(name: str, slug: str, db: DBDep):
    svc = PlanetService(db)
    planet = svc.create(name=name, slug=slug)
    return {
        'id': planet.id,
        'name': planet.name,
        'slug': planet.slug,
        'stats': planet.stats,
    }

@router.get('/{slug}')
def get_planet(slug: str, db: DBDep):
    planet = PlanetService(db).fetch(slug)
    if not planet:
        raise HTTPException(status_code=404, detail='planet not found')
    return {
        'id': planet.id,
        'name': planet.name,
        'slug': planet.slug,
        'stats': planet.stats,
    }
