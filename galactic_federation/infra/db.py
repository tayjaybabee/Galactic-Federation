from __future__ import annotations
from typing import Generator
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from ..core.settings import get_settings

class Base(DeclarativeBase):
    pass

_engine = create_engine(get_settings().db_dsn, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine, expire_on_commit=False)


def get_db() -> Generator:
    """Yield a SQLAlchemy session and ensure proper cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
