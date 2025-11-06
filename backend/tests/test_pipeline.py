from __future__ import annotations

import numpy as np

from backend.services.detection import FaceDetector
from backend.services.embedding import FaceEmbedder
from backend.services.emotion_model import EmotionClassifier
from backend.services.pipeline import FacePipeline
from backend.services.storage import EmbeddingStore
from backend.utils.postprocessing import Detection


class DummyDetector(FaceDetector):
    def __init__(self):  # noqa: D401
        super().__init__("backend/models/detection.onnx")

    def detect(self, image):  # noqa: ANN001
        return [Detection(bbox=[0, 0, image.shape[1], image.shape[0]], landmarks={}, score=0.99)]


def test_pipeline_returns_result():
    image = np.zeros((8, 8, 3), dtype=np.uint8)
    pipeline = FacePipeline(DummyDetector(), FaceEmbedder("backend/models/arcface.onnx"), EmotionClassifier("backend/models/emotion.onnx"), EmbeddingStore())
    result = pipeline.run(image)
    assert len(result.detections) == 1
    assert len(result.recognitions) == 1
    assert result.timings["total"] >= 0.0
