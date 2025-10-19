from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, String, JSON, ForeignKey, DateTime, func, Boolean, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .db import Base

class Planet(Base):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(96), unique=True, nullable=False)
    sector_id: Mapped[int | None] = mapped_column(ForeignKey('sector.id'), nullable=True)
    stats: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    sector = relationship('Sector', back_populates='planets')

class Sector(Base):
    __tablename__ = 'sector'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(96), unique=True, nullable=False)
    charter_md: Mapped[str] = mapped_column(Text, default='')

    planets = relationship('Planet', back_populates='sector')

class Issue(Base):
    __tablename__ = 'issue'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(160))
    prompt: Mapped[str] = mapped_column(String)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

class IssueOption(Base):
    __tablename__ = 'issue_option'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey('issue.id'), index=True)
    text: Mapped[str] = mapped_column(String)
    effects_json: Mapped[dict] = mapped_column(JSON, default=dict)

class PendingIssue(Base):
    __tablename__ = 'pending_issue'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), index=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey('issue.id'), index=True)
    expires_at: Mapped[str] = mapped_column(DateTime(timezone=True))
    seed_data_json: Mapped[dict] = mapped_column(JSON, default=dict)

class Decision(Base):
    __tablename__ = 'decision'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), index=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey('issue.id'), index=True)
    option_id: Mapped[int] = mapped_column(ForeignKey('issue_option.id'))
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    effects_applied_json: Mapped[dict] = mapped_column(JSON, default=dict)
