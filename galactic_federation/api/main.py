from __future__ import annotations
import logging
from fastapi import FastAPI
from ..core.logging import configure_logging
from ..core.settings import get_settings
from .routes import planets, issues, regions

configure_logging(logging.INFO)
settings = get_settings()
app = FastAPI(title='Galactic Federation', version='0.1.0')

app.include_router(planets.router)
app.include_router(issues.router)
app.include_router(regions.router)

@app.get('/')
def root():
    return {'name': 'Galactic Federation', 'env': settings.env}
