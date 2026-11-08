import shutil
from pathlib import Path

import pytest
from sqlalchemy import func, select, text
from sqlalchemy.exc import DBAPIError

from app.ingest import import_sources, read_corpus
from app.knowledge import ResearchChunk, ResearchSourceVersion

pytestmark = pytest.mark.integration
CORPUS = Path(__file__).resolve().parents[2] / "data/curated"


def test_missing_notes_directory_is_not_a_corpus_update(tmp_path):
    shutil.copytree(CORPUS / "rule_reviews", tmp_path / "rule_reviews")
    with pytest.raises(ValueError, match="Missing research directory"):
        read_corpus(tmp_path)


def test_incremental_import_history_and_no_approval(database, tmp_path):
    shutil.copytree(CORPUS / "research", tmp_path / "research")
    shutil.copytree(CORPUS / "rule_reviews", tmp_path / "rule_reviews")
    assert import_sources(database, tmp_path)["created_versions"] == 40
    assert import_sources(database, tmp_path)["unchanged_sources"] == 40
    assert database.scalar(select(func.count()).select_from(ResearchChunk)) == 122
    path = tmp_path / "research/source_notes.yaml"
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "Rotation fights disease", "Updated note: rotation fights disease", 1
        ),
        encoding="utf-8",
    )
    assert import_sources(database, tmp_path)["created_versions"] == 1
    assert database.scalar(select(func.count()).select_from(ResearchSourceVersion)) == 41
    assert set(database.scalars(select(ResearchSourceVersion.review_status))) == {"unreviewed"}
    with pytest.raises(DBAPIError), database.begin_nested():
        database.execute(text("UPDATE research_source_versions SET review_status = 'approved'"))


def test_bad_reference_and_partial_failure_roll_back(database, tmp_path):
    shutil.copytree(CORPUS / "research", tmp_path / "research")
    shutil.copytree(CORPUS / "rule_reviews", tmp_path / "rule_reviews")
    path = tmp_path / "research/source_notes.yaml"
    original = path.read_text(encoding="utf-8")
    path.write_text(
        original.replace("source: SRC-SARE-ROTATION", "source: SRC-MISSING", 1), encoding="utf-8"
    )
    with pytest.raises(ValueError):
        import_sources(database, tmp_path)
    assert database.scalar(select(func.count()).select_from(ResearchSourceVersion)) == 0
    path.write_text(original, encoding="utf-8")
    with pytest.raises(RuntimeError), database.begin_nested():
        import_sources(database, tmp_path)
        raise RuntimeError("Simulated interruption before commit")
    assert database.scalar(select(func.count()).select_from(ResearchSourceVersion)) == 0
    assert import_sources(database, tmp_path)["created_versions"] == 40
