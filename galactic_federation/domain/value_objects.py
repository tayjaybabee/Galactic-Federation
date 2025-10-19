from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class EffectOp:
    op: str  # 'add' | 'mul' | 'tag'
    path: str
    value: float | str
