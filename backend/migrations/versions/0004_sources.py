"""Immutable, unreviewed research versions; no embeddings or executable rules."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "0004_sources"
down_revision = "0003_growing"


def upgrade():
    op.create_table("research_sources", sa.Column("id", sa.String(100), primary_key=True))
    op.create_table(
        "research_source_versions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "source_id", sa.String(100), sa.ForeignKey("research_sources.id"), nullable=False
        ),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("source_metadata", JSONB, nullable=False),
        sa.Column("import_provenance", JSONB, nullable=False),
        sa.Column("review_status", sa.String(20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("source_id", "version"),
        sa.UniqueConstraint("source_id", "content_hash"),
        sa.CheckConstraint("review_status = 'unreviewed'", name="source_review_disabled"),
    )
    op.create_index(
        "ix_research_source_versions_source_id", "research_source_versions", ["source_id"]
    )
    op.create_table(
        "research_chunks",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "source_version_id",
            sa.Uuid(),
            sa.ForeignKey("research_source_versions.id"),
            nullable=False,
        ),
        sa.Column("note_id", sa.String(100), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("locator", sa.String(), nullable=False),
        sa.Column("topics", JSONB, nullable=False),
        sa.UniqueConstraint("source_version_id", "note_id"),
    )
    op.create_index(
        "ix_research_chunks_source_version_id", "research_chunks", ["source_version_id"]
    )
    op.execute("""CREATE FUNCTION reject_research_mutation() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN RAISE EXCEPTION 'Research history is immutable'; END; $$""")
    for table in ["research_source_versions", "research_chunks"]:
        op.execute(
            f"CREATE TRIGGER immutable_history BEFORE UPDATE OR DELETE ON {table} FOR EACH ROW EXECUTE FUNCTION reject_research_mutation()"
        )


def downgrade():
    op.drop_table("research_chunks")
    op.drop_table("research_source_versions")
    op.drop_table("research_sources")
    op.execute("DROP FUNCTION reject_research_mutation()")
