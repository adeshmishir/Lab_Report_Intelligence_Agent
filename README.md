# LabLens

LLM-powered lab report intelligence agent.

> Demo workspace · Sample reports only

## Current phase

**Phase 1** — Project foundation and UI.

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
