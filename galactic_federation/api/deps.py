from __future__ import annotations
from fastapi import Depends
from ..core.settings import get_settings, Settings
from ..infra.db import get_db
from typing import Annotated
from sqlalchemy.orm import Session

SettingsDep = Annotated[Settings, Depends(get_settings)]
DBDep = Annotated[Session, Depends(get_db)]
