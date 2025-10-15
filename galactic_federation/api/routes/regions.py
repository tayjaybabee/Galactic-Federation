from __future__ import annotations
from fastapi import APIRouter, HTTPException
from ..deps import DBDep
from ...domain.services.region_service import RegionService

router = APIRouter(prefix='/sectors', tags=['sectors'])

@router.get('/{slug}')
def get_sector(slug: str, db: DBDep):
    sector = RegionService(db).fetch(slug)
    if not sector:
        raise HTTPException(status_code=404, detail='sector not found')
    return {'name': sector.name, 'slug': sector.slug, 'charter_md': sector.charter_md}
