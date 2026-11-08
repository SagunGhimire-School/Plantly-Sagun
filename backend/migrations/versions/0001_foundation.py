"""Enable pgvector without selecting an embedding model or dimension."""

from alembic import op

revision = "0001_foundation"
down_revision = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade():
    # Shared database capabilities survive application rollback.
    pass
