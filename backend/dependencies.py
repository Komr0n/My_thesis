from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from backend.services.detection import FaceDetector
from backend.services.embedding import FaceEmbedder
from backend.services.emotion_model import EmotionClassifier
from backend.services.pipeline import FacePipeline
from backend.services.storage import EmbeddingStore


@lru_cache(maxsize=1)
def get_storage() -> EmbeddingStore:
    threshold = float(os.getenv("EMBEDDING_THRESHOLD", "0.6"))
    return EmbeddingStore(threshold=threshold)


@lru_cache(maxsize=1)
def get_detector() -> FaceDetector:
    model_path = Path(os.getenv("DETECTION_MODEL_PATH", "backend/models/detection.onnx"))
    return FaceDetector(model_path)


@lru_cache(maxsize=1)
def get_embedder() -> FaceEmbedder:
    model_path = Path(os.getenv("EMBEDDING_MODEL_PATH", "backend/models/arcface.onnx"))
    return FaceEmbedder(model_path)


@lru_cache(maxsize=1)
def get_emotion_model() -> EmotionClassifier:
    model_path = Path(os.getenv("EMOTION_MODEL_PATH", "backend/models/emotion.onnx"))
    return EmotionClassifier(model_path)


@lru_cache(maxsize=1)
def get_pipeline() -> FacePipeline:
    return FacePipeline(get_detector(), get_embedder(), get_emotion_model(), get_storage())
