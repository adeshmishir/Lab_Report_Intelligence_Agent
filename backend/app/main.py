from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.core.config import Settings, get_settings
from app.core.database import SessionLocal
from app.core.errors import LabLensError
from app.api.routes.reports import router as reports_router
from app.api.routes.ask import router as ask_router
from app.api.routes.trends import router as trends_router
from app.api.routes.corrections import router as corrections_router


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(LabLensError)
    async def app_error_handler(request: Request, exc: LabLensError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.code, "message": exc.message}},
        )

    @app.exception_handler(HTTPException)
    async def http_error_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": "INVALID_FILE", "message": str(exc.detail)}},
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"error": {"code": "DATABASE_ERROR", "message": "Something went wrong. Please try again."}},
        )

    @app.get("/health")
    def health_check():
        try:
            with SessionLocal() as db:
                db.execute(text("SELECT 1"))
            return {"status": "ok", "database": "ok"}
        except Exception:
            return JSONResponse(status_code=503, content={"status": "error", "database": "unavailable"})

    app.include_router(reports_router)
    app.include_router(ask_router)
    app.include_router(trends_router)
    app.include_router(corrections_router)

    return app


app = create_app()