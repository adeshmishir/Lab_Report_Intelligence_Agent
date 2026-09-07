from datetime import date

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    report_id: int | None = Field(default=None, gt=0)


class Citation(BaseModel):
    report_id: int
    result_id: int
    filename: str
    report_date: date | None = None
    test_name: str
    evidence: str


class AskResponse(BaseModel):
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    safety_notice: str | None = None
    tool_name: str | None = None
    tool_arguments: dict[str, str | int | None] = Field(default_factory=dict)
    evidence_result_ids: list[int] = Field(default_factory=list)