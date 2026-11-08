"""Growing records and a resumable draft per grower."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "0003_growing"
down_revision = "0002_identity"


def upgrade():
    op.create_table(
        "plots",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("area_m2", sa.Numeric(14, 4), nullable=False),
        sa.Column("location_data", JSONB, nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("area_m2 > 0", name="plot_positive_area"),
        sa.UniqueConstraint("id", "user_id"),
    )
    op.create_index("ix_plots_user_id", "plots", ["user_id"])
    op.create_table(
        "seasons",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("label", sa.String(100), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.Date()),
        sa.Column("end_date", sa.Date()),
        sa.Column("status", sa.String(20), nullable=False),
        sa.UniqueConstraint("id", "user_id"),
        sa.CheckConstraint(
            "end_date IS NULL OR start_date IS NULL OR end_date >= start_date",
            name="season_date_order",
        ),
    )
    op.create_index("ix_seasons_user_id", "seasons", ["user_id"])
    op.create_table(
        "plot_seasons",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("plot_id", sa.Uuid(), nullable=False),
        sa.Column("season_id", sa.Uuid(), nullable=False),
        sa.Column("goals", JSONB, nullable=False),
        sa.Column("budget_amount", sa.Numeric(12, 2)),
        sa.Column("currency", sa.String(3)),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.UniqueConstraint("plot_id", "season_id"),
        sa.ForeignKeyConstraint(
            ["plot_id", "user_id"], ["plots.id", "plots.user_id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["season_id", "user_id"], ["seasons.id", "seasons.user_id"], ondelete="CASCADE"
        ),
    )
    for column in ["user_id", "plot_id", "season_id"]:
        op.create_index(f"ix_plot_seasons_{column}", "plot_seasons", [column])
    op.create_table(
        "onboarding_drafts",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Uuid(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("draft_data", JSONB, nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("schema_version", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("step", sa.Integer(), nullable=False),
        sa.Column("completed_ids", JSONB),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade():
    for table in ["onboarding_drafts", "plot_seasons", "seasons", "plots"]:
        op.drop_table(table)
