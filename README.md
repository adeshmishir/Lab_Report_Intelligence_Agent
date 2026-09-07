# LabLens

LLM-powered lab report intelligence agent.

> Demo workspace · Sample reports only

## Current phase

**Phase 3** — Database, normalization, and data quality.

## Planned capabilities

- PDF/image report ingestion
- Structured lab result extraction
- Grounded Q&A
- Deterministic tool calling
- Longitudinal comparison
- Ambiguity handling
- Correction workflow
- Safety and prompt-injection protection

## Project structure

```
/
├── frontend/          React + Vite + Tailwind CSS
├── backend/           FastAPI + SQLAlchemy + PostgreSQL
├── docker-compose.yml
└── README.md
```

## Running locally

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend runs at `http://localhost:8000`.

Health check: `GET http://localhost:8000/health`

### Docker

```bash
docker-compose up
```

### Environment variables

Copy `backend/.env.example` to `backend/.env`:

```
APP_NAME=LabLens
DEBUG=false
DATABASE_URL=postgresql://lablens:lablens@localhost:5432/lablens
CORS_ORIGINS=["http://localhost:5173"]
```

## Notes

- Phase 1 uses **sample/demo data only**. No real medical data is processed.
- The application does not diagnose conditions or recommend treatments.
- Backend functionality (OCR, extraction, LLM, embeddings) will be implemented in Phase 2.

## Phase 3 architecture

```text
Upload
	↓
Extraction
	↓
Pydantic validation
	↓
Test-name and unit normalization
	↓
Reference parsing and data quality
	↓
PostgreSQL (Report → LabResult)
```

Reports and results are managed by Alembic migrations. Original names, raw text,
reference text, confidence, and quality state are retained for auditability.
Numeric and qualitative values use separate fields. Duplicate results remain
stored; identical duplicates and conflicting values are classified deterministically.

Phase 3 endpoints include `GET /api/reports`, `GET /api/reports/{report_id}`,
and `GET /api/reports/{report_id}/results?test_name=HbA1c`.

### Phase 3 verification

```bash
cd backend
python -m pytest tests -q
cd ../frontend
npm test
npm run build
```

The schema includes one seeded demo user for the `User -> Report -> LabResult`
relationship. No authentication is required in this phase.

## Phase 4 architecture

```text
Question
	↓
Safety and intent checks
	↓
Deterministic retrieval tools
	↓
Report/result evidence
	↓
Optional grounded LLM composition
	↓
Answer with citations
```

Phase 4 adds `POST /api/ask`. It supports latest-result, trend, and comparison
questions, optionally scoped with `report_id`. The service retrieves only
processed results belonging to the demo user, preserves incomplete/conflicting
quality states, and returns report/result citations. Without `LLM_API_KEY`, a
deterministic answer is returned; with a key, the LLM may compose from the
retrieved evidence only. Diagnosis, treatment, prescription, and prompt-injection
requests receive a safety response instead of an unsupported answer.

## Phase 5 architecture

The dashboard, reports list, report details, upload flow, and trends page now
read from the backend instead of demo-only state. Uploading a file refreshes
the report list after successful persistence. `GET /api/trends` groups numeric
values by normalized test name and preserves report dates, units, and quality
states for the trend view.
