"""Versioned source storage. Importing content never makes it scientifically eligible."""

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.auth import now
from app.db import Base


class ResearchSource(Base):
    __tablename__ = "research_sources"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)


class ResearchSourceVersion(Base):
    __tablename__ = "research_source_versions"
    __table_args__ = (
        UniqueConstraint("source_id", "version"),
        UniqueConstraint("source_id", "content_hash"),
        CheckConstraint("review_status = 'unreviewed'", name="source_review_disabled"),
    )
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    source_id: Mapped[str] = mapped_column(ForeignKey("research_sources.id"), index=True)
    version: Mapped[int]
    content_hash: Mapped[str] = mapped_column(String(64))
    source_metadata: Mapped[dict] = mapped_column(JSONB)
    import_provenance: Mapped[dict] = mapped_column(JSONB)
    review_status: Mapped[str] = mapped_column(String(20), default="unreviewed")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class ResearchChunk(Base):
    __tablename__ = "research_chunks"
    __table_args__ = (UniqueConstraint("source_version_id", "note_id"),)
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    source_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("research_source_versions.id"), index=True
    )
    note_id: Mapped[str] = mapped_column(String(100))
    content: Mapped[str]
    locator: Mapped[str]
    topics: Mapped[list] = mapped_column(JSONB)
