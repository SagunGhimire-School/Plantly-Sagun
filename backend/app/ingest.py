"""Manual atomic import of source catalog and paraphrased notes, always unreviewed.

Run from backend: python -m app.ingest --root ../data/curated
Numeric datasets/fixtures are excluded pending validated per-kind provenance.
"""

import argparse
import hashlib
import json
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, TypeAdapter
from sqlalchemy import func, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db import engine
from app.knowledge import ResearchChunk, ResearchSource, ResearchSourceVersion


class SourceRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    id: str = Field(pattern=r"^SRC-[A-Z0-9-]+$", max_length=100)
    title: str = Field(min_length=1, max_length=1000)
    publisher: str = Field(max_length=1000)
    year: int | None
    url: str = Field(max_length=2000)
    verified: bool  # Legacy metadata only, never mapped to approval.


class NoteRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    id: str = Field(min_length=1, max_length=100)
    source: str
    page: str = Field(min_length=1, max_length=1000)
    topics: list[str] = Field(max_length=50)
    note: str = Field(min_length=1, max_length=20000)
    verified: bool


def load_rows(path, model):
    raw = path.read_bytes()
    if len(raw) > 5_000_000:
        raise ValueError(f"Source file too large: {path.name}")
    records = TypeAdapter(list[model]).validate_python(yaml.safe_load(raw))
    ids = [record.id for record in records]
    if len(ids) != len(set(ids)):
        raise ValueError(f"Duplicate IDs in {path.name}")
    return records, hashlib.sha256(raw).hexdigest()


def read_corpus(root):
    root = Path(root)
    if not (root / "research").is_dir():
        raise ValueError("Missing research directory; refusing to import an incomplete corpus")
    sources, source_hash = load_rows(root / "rule_reviews/sources.yaml", SourceRow)
    source_ids = {source.id for source in sources}
    for source in sources:
        if source.url:
            TypeAdapter(HttpUrl).validate_python(source.url)
    notes, provenance, note_ids = [], {"rule_reviews/sources.yaml": source_hash}, set()
    for path in sorted((root / "research").glob("*.yaml")):
        rows, checksum = load_rows(path, NoteRow)
        provenance[path.relative_to(root).as_posix()] = checksum
        for row in rows:
            if row.id in note_ids or row.source not in source_ids:
                raise ValueError(f"Duplicate note or missing source: {row.id}")
            note_ids.add(row.id)
            notes.append(row)
    return sources, notes, provenance


def import_sources(db, root):
    sources, notes, provenance = read_corpus(root)
    db.execute(text("SELECT pg_advisory_xact_lock(71823941)"))
    result = {
        "created_versions": 0,
        "unchanged_sources": 0,
        "review_status": "unreviewed",
        "notes": len(notes),
    }
    for source in sources:
        source_notes = sorted(
            [note for note in notes if note.source == source.id], key=lambda note: note.id
        )
        snapshot = {
            "source": source.model_dump(),
            "notes": [note.model_dump() for note in source_notes],
        }
        checksum = hashlib.sha256(
            json.dumps(snapshot, sort_keys=True, ensure_ascii=False).encode()
        ).hexdigest()
        existing = db.scalar(
            select(ResearchSourceVersion).where(
                ResearchSourceVersion.source_id == source.id,
                ResearchSourceVersion.content_hash == checksum,
            )
        )
        if existing:
            result["unchanged_sources"] += 1
            continue
        if db.get(ResearchSource, source.id) is None:
            db.add(ResearchSource(id=source.id))
            db.flush()
        number = (
            db.scalar(
                select(func.max(ResearchSourceVersion.version)).where(
                    ResearchSourceVersion.source_id == source.id
                )
            )
            or 0
        )
        version = ResearchSourceVersion(
            source_id=source.id,
            version=number + 1,
            content_hash=checksum,
            source_metadata={**source.model_dump(), "license_status": "unknown"},
            import_provenance=provenance,
        )
        db.add(version)
        db.flush()
        for note in source_notes:
            db.add(
                ResearchChunk(
                    source_version_id=version.id,
                    note_id=note.id,
                    content=note.note,
                    locator=note.page,
                    topics=note.topics,
                )
            )
        result["created_versions"] += 1
    db.flush()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("../data/curated"))
    args = parser.parse_args()
    try:
        with Session(engine) as db, db.begin():
            result = import_sources(db, args.root)
        print(json.dumps({"status": "success", **result}))
    except (ValueError, yaml.YAMLError) as error:
        print(json.dumps({"status": "failed", "validation": str(error)}))
        raise SystemExit(1) from None
    except OSError:
        print(json.dumps({"status": "failed", "validation": "Source files could not be read."}))
        raise SystemExit(1) from None
    except SQLAlchemyError:
        print(
            json.dumps(
                {
                    "status": "failed",
                    "validation": "Database import failed; the transaction was rolled back. Check connectivity and migrations.",
                }
            )
        )
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
