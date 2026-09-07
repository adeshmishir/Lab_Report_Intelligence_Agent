"""add correction provenance and critical-result flags

Revision ID: 0005_corrections_and_critical
Revises: 0004_upload_hardening
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0005_corrections_and_critical"
down_revision: Union[str, None] = "0004_upload_hardening"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE dataquality ADD VALUE IF NOT EXISTS 'critical'")
    op.add_column("lab_results", sa.Column("value_numeric_original", sa.Float(), nullable=True))
    op.add_column("lab_results", sa.Column("value_text_original", sa.String(length=255), nullable=True))
    op.add_column("lab_results", sa.Column("critical", sa.Boolean(), nullable=True))
    op.add_column("lab_results", sa.Column("correction_note", sa.Text(), nullable=True))
    op.add_column("lab_results", sa.Column("corrected_at", sa.DateTime(), nullable=True))
    op.execute("UPDATE lab_results SET value_numeric_original = value_numeric, value_text_original = value_text, critical = FALSE WHERE value_numeric_original IS NULL AND value_text_original IS NULL")
    op.execute("UPDATE lab_results SET critical = FALSE WHERE critical IS NULL")
    op.alter_column("lab_results", "critical", nullable=False)


def downgrade() -> None:
    op.drop_column("lab_results", "corrected_at")
    op.drop_column("lab_results", "correction_note")
    op.drop_column("lab_results", "critical")
    op.drop_column("lab_results", "value_text_original")
    op.drop_column("lab_results", "value_numeric_original")