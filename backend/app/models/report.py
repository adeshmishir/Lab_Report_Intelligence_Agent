from datetime import date, datetime
from sqlalchemy import String, Text, Date, DateTime, Float, ForeignKey, Enum, Integer, Index, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

import enum


class ReportStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class Confidence(str, enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class DataQuality(str, enum.Enum):
    GOOD = "good"
    MISSING_VALUE = "missing_value"
    MISSING_UNIT = "missing_unit"
    MISSING_REFERENCE_RANGE = "missing_reference_range"
    AMBIGUOUS_VALUE = "ambiguous_value"
    DUPLICATE_TEST = "duplicate_test"
    CONFLICTING_VALUES = "conflicting_values"
    UNREADABLE = "unreadable"
    INVALID = "invalid"
    CRITICAL = "critical"


def _enum_values(klass):
    return [item.value for item in klass]


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False, index=True)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(64), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    report_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[ReportStatus] = mapped_column(
        Enum(ReportStatus, values_callable=_enum_values), nullable=False, default=ReportStatus.PROCESSED
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="reports")
    patient: Mapped["Patient"] = relationship(back_populates="reports")

    results: Mapped[list["LabResult"]] = relationship(
        back_populates="report", cascade="all, delete-orphan", order_by="LabResult.id"
    )


class LabResult(Base):
    __tablename__ = "lab_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"), nullable=False, index=True)
    test_name_original: Mapped[str] = mapped_column(String(255), nullable=False)
    test_name_normalized: Mapped[str] = mapped_column(String(255), nullable=False)
    value_numeric: Mapped[float | None] = mapped_column(Float, nullable=True)
    value_text: Mapped[str | None] = mapped_column(String(255), nullable=True)
    value_numeric_original: Mapped[float | None] = mapped_column(Float, nullable=True)
    value_text_original: Mapped[str | None] = mapped_column(String(255), nullable=True)
    unit: Mapped[str | None] = mapped_column(String(64), nullable=True)
    reference_low: Mapped[float | None] = mapped_column(Float, nullable=True)
    reference_high: Mapped[float | None] = mapped_column(Float, nullable=True)
    reference_text: Mapped[str | None] = mapped_column(String(255), nullable=True)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[Confidence] = mapped_column(
        Enum(Confidence, values_callable=_enum_values), nullable=False
    )
    data_quality: Mapped[DataQuality] = mapped_column(
        Enum(DataQuality, values_callable=_enum_values), nullable=False
    )
    critical: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    correction_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    corrected_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    report: Mapped[Report] = relationship(back_populates="results")


Index("ix_reports_report_date", Report.report_date)
Index("ix_lab_results_test_name_normalized", LabResult.test_name_normalized)