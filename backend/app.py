from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db.database import Base, engine
from backend.routers import detect, emotion, enroll, health, persons, pipeline, recognize

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(title="Face Emotion Pipeline API", version="0.1.0", openapi_url="/api/openapi.json")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # in production override via env var
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix="/api")
    app.include_router(detect.router, prefix="/api")
    app.include_router(recognize.router, prefix="/api")
    app.include_router(emotion.router, prefix="/api")
    app.include_router(pipeline.router, prefix="/api")
    app.include_router(enroll.router, prefix="/api")
    app.include_router(persons.router, prefix="/api")

    return app


def init_models() -> None:
    models_path = Path(__file__).parent / "models"
    if not models_path.exists():
        logger.warning("Model directory %s does not exist", models_path)
    else:
        logger.info("Model directory available at %s", models_path)


Base.metadata.create_all(bind=engine)
init_models()
app = create_app()
