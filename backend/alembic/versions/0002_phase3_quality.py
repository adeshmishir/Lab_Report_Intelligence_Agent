"""add phase 3 normalized values and quality metadata

Revision ID: 0002_phase3_quality
Revises: 0001_initial
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_phase3_quality"
down_revision: Union[str, None] = "0001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE dataquality ADD VALUE IF NOT EXISTS 'missing_value'")
    op.execute("ALTER TYPE dataquality ADD VALUE IF NOT EXISTS 'invalid'")
    op.alter_column("lab_results", "value", new_column_name="value_numeric")
    op.add_column("lab_results", sa.Column("value_text", sa.String(length=255), nullable=True))
    op.add_column("lab_results", sa.Column("reference_text", sa.String(length=255), nullable=True))
    op.add_column("reports", sa.Column("updated_at", sa.DateTime(), nullable=True))
    op.add_column("lab_results", sa.Column("updated_at", sa.DateTime(), nullable=True))
    op.execute("UPDATE reports SET updated_at = created_at WHERE updated_at IS NULL")
    op.execute("UPDATE lab_results SET updated_at = created_at WHERE updated_at IS NULL")
    op.alter_column("reports", "updated_at", nullable=False)
    op.alter_column("lab_results", "updated_at", nullable=False)
    op.create_index("ix_reports_report_date", "reports", ["report_date"])
    op.create_index("ix_lab_results_test_name_normalized", "lab_results", ["test_name_normalized"])


def downgrade() -> None:
    op.drop_index("ix_lab_results_test_name_normalized", table_name="lab_results")
    op.drop_index("ix_reports_report_date", table_name="reports")
    op.drop_column("lab_results", "updated_at")
    op.drop_column("reports", "updated_at")
    op.drop_column("lab_results", "reference_text")
    op.drop_column("lab_results", "value_text")
    op.alter_column("lab_results", "value_numeric", new_column_name="value")