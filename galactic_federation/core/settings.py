from __future__ import annotations
import os
from functools import lru_cache
from pydantic import BaseModel

class Settings(BaseModel):
    """Application settings loaded from environment.

    Properties:
        env: Execution environment label.
        db_dsn: SQLAlchemy DSN for PostgreSQL.
        redis_url: Redis connection URL.
        secret_key: App secret for signing.
        issues_per_day: How many issues a planet receives daily.
        feature_flags: Comma-separated list of enabled features.
    """

    env: str = os.getenv('GF_ENV', 'local')
    db_dsn: str = os.getenv('GF_DB_DSN', 'postgresql+psycopg2://postgres:postgres@localhost:5432/galactic_federation')
    redis_url: str = os.getenv('GF_REDIS_URL', 'redis://localhost:6379/0')
    secret_key: str = os.getenv('GF_SECRET_KEY', 'change_me')
    issues_per_day: int = int(os.getenv('GF_ISSUES_PER_DAY', '3'))
    feature_flags: str = os.getenv('GF_FEATURE_FLAGS', 'issues,regions,assembly')

    @property
    def flags(self) -> set[str]:
        return {f.strip() for f in self.feature_flags.split(',') if f.strip()}

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
