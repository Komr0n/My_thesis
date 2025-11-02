from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List, Sequence

import numpy as np

from backend.services.detection import FaceDetector
from backend.services.embedding import FaceEmbedder
from backend.services.emotion_model import EmotionClassifier
from backend.services.storage import EmbeddingStore
from backend.utils.metrics import TimingCollector
from backend.utils.postprocessing import Detection, Emotion, Recognition
from backend.utils.preprocessing import align_face

logger = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    detections: List[Detection]
    recognitions: List[Recognition | None]
    emotions: List[Emotion | None]
    timings: dict[str, float]


class FacePipeline:
    def __init__(
        self,
        detector: FaceDetector,
        embedder: FaceEmbedder,
        emotion_model: EmotionClassifier,
        storage: EmbeddingStore,
    ) -> None:
        self.detector = detector
        self.embedder = embedder
        self.emotion_model = emotion_model
        self.storage = storage

    def run(
        self,
        image: np.ndarray,
        recognize: bool = True,
        emotions: bool = True,
        top_k: int = 3,
    ) -> PipelineResult:
        timings = TimingCollector()
        with timings.track("detect"):
            detections = self.detector.detect(image)
        crops: list[np.ndarray] = []
        for detection in detections:
            x, y, w, h = map(int, detection.bbox)
            crop = image[y : y + h, x : x + w]
            crop = align_face({k: tuple(v) for k, v in detection.landmarks.items() if v}, crop)
            crops.append(crop)

        embeddings: list[np.ndarray] = []
        if recognize and crops:
            with timings.track("embed"):
                embeddings = self.embedder.embed(crops)
        recognitions: list[Recognition | None] = [None] * len(detections)
        if recognize and embeddings:
            with timings.track("recognize"):
                recognitions = []
                for embedding in embeddings:
                    matches = self.storage.topk_similar(embedding, top_k=top_k)
                    if matches:
                        best = matches[0]
                        recognitions.append(
                            Recognition(
                                person=best.person,
                                similarity=best.similarity,
                                embedding_norm=best.embedding_norm,
                            )
                        )
                    else:
                        recognitions.append(None)

        emotions_out: list[Emotion | None] = [None] * len(detections)
        if emotions and crops:
            with timings.track("emotion"):
                emotions_out = self.emotion_model.classify(crops)
        timings.timings["total"] = timings.total()
        return PipelineResult(detections, recognitions, emotions_out, timings.timings)
