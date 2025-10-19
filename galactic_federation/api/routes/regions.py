from __future__ import annotations
from fastapi import APIRouter, HTTPException
from ..deps import DBDep
from ...domain.services.sector_service import SectorService

router = APIRouter(prefix='/sectors', tags=['sectors'])

@router.get('/{slug}')
def get_sector(slug: str, db: DBDep):
    if sector := SectorService(db).fetch(slug):
        return {'name': sector.name, 'slug': sector.slug, 'charter_md': sector.charter_md}
    raise HTTPException(status_code=404, detail='sector not found')
