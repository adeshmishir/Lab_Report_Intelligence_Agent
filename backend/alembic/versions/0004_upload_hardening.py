"""add report content fingerprints

Revision ID: 0004_upload_hardening
Revises: 0003_demo_user
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0004_upload_hardening"
down_revision: Union[str, None] = "0003_demo_user"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("reports", sa.Column("content_hash", sa.String(length=64), nullable=True))
    op.execute("UPDATE reports SET content_hash = md5(raw_text) WHERE content_hash IS NULL")
    op.alter_column("reports", "content_hash", nullable=False)
    op.create_index("ix_reports_content_hash", "reports", ["content_hash"])


def downgrade() -> None:
    op.drop_index("ix_reports_content_hash", table_name="reports")
    op.drop_column("reports", "content_hash")