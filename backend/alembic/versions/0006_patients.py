"""add patient ownership to reports

Revision ID: 0006_patients
Revises: 0005_corrections_and_critical
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0006_patients"
down_revision: Union[str, None] = "0005_corrections_and_critical"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "patients",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("normalized_name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_patients_user_id", "patients", ["user_id"])
    op.create_index("ix_patients_normalized_name", "patients", ["normalized_name"])
    op.execute("INSERT INTO patients (id, user_id, name, normalized_name, created_at, updated_at) VALUES (1, 1, 'Demo Patient', 'demo patient', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)")
    op.add_column("reports", sa.Column("patient_id", sa.Integer(), nullable=True))
    op.execute("UPDATE reports SET patient_id = 1 WHERE patient_id IS NULL")
    op.alter_column("reports", "patient_id", nullable=False)
    op.create_foreign_key("fk_reports_patient_id_patients", "reports", "patients", ["patient_id"], ["id"])
    op.create_index("ix_reports_patient_id", "reports", ["patient_id"])


def downgrade() -> None:
    op.drop_index("ix_reports_patient_id", table_name="reports")
    op.drop_constraint("fk_reports_patient_id_patients", "reports", type_="foreignkey")
    op.drop_column("reports", "patient_id")
    op.drop_index("ix_patients_normalized_name", table_name="patients")
    op.drop_index("ix_patients_user_id", table_name="patients")
    op.drop_table("patients")