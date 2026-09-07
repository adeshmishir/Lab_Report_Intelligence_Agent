"""initial schema: reports and lab_results

Revision ID: 0001_initial
Revises:
Create Date: 2026-09-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    report_status = sa.Enum(
        "uploaded", "processing", "processed", "failed", name="reportstatus"
    )
    confidence = sa.Enum("high", "medium", "low", name="confidence")
    data_quality = sa.Enum(
        "good",
        "missing_value",
        "missing_unit",
        "missing_reference_range",
        "ambiguous_value",
        "duplicate_test",
        "conflicting_values",
        "unreadable",
        "invalid",
        name="dataquality",
    )

    op.create_table(
        "reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("mime_type", sa.String(length=64), nullable=False),
        sa.Column("report_date", sa.Date(), nullable=True),
        sa.Column("raw_text", sa.Text(), nullable=False),
        sa.Column("status", report_status, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "lab_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("report_id", sa.Integer(), sa.ForeignKey("reports.id"), nullable=False),
        sa.Column("test_name_original", sa.String(length=255), nullable=False),
        sa.Column("test_name_normalized", sa.String(length=255), nullable=False),
        sa.Column("value", sa.Float(), nullable=True),
        sa.Column("unit", sa.String(length=64), nullable=True),
        sa.Column("reference_low", sa.Float(), nullable=True),
        sa.Column("reference_high", sa.Float(), nullable=True),
        sa.Column("raw_text", sa.Text(), nullable=False),
        sa.Column("confidence", confidence, nullable=False),
        sa.Column("data_quality", data_quality, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_lab_results_report_id", "lab_results", ["report_id"])


def downgrade() -> None:
    op.drop_table("lab_results")
    op.drop_table("reports")
    op.execute("DROP TYPE IF EXISTS reportstatus")
    op.execute("DROP TYPE IF EXISTS confidence")
    op.execute("DROP TYPE IF EXISTS dataquality")