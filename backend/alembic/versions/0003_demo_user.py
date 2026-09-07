"""add the single demo user and report ownership

Revision ID: 0003_demo_user
Revises: 0002_phase3_quality
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0003_demo_user"
down_revision: Union[str, None] = "0002_phase3_quality"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.execute("INSERT INTO users (id, display_name, created_at) VALUES (1, 'Demo User', CURRENT_TIMESTAMP)")
    op.add_column("reports", sa.Column("user_id", sa.Integer(), nullable=True))
    op.execute("UPDATE reports SET user_id = 1 WHERE user_id IS NULL")
    op.alter_column("reports", "user_id", nullable=False)
    op.create_foreign_key("fk_reports_user_id_users", "reports", "users", ["user_id"], ["id"])
    op.create_index("ix_reports_user_id", "reports", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_reports_user_id", table_name="reports")
    op.drop_constraint("fk_reports_user_id_users", "reports", type_="foreignkey")
    op.drop_column("reports", "user_id")
    op.drop_table("users")