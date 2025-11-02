from __future__ import annotations

from __future__ import annotations

import base64
from unittest.mock import patch

import numpy as np
from fastapi.testclient import TestClient

from backend.app import app
from backend.services.pipeline import PipelineResult
from backend.utils.postprocessing import Detection, Emotion, Recognition

client = TestClient(app)


def create_blank_image_base64() -> str:
    import cv2

    image = np.zeros((10, 10, 3), dtype=np.uint8)
    success, buffer = cv2.imencode(".jpg", image)
    assert success
    payload = base64.b64encode(buffer).decode()
    return f"data:image/jpeg;base64,{payload}"


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_pipeline_endpoint_returns_structure():
    image_payload = {"image_base64": create_blank_image_base64()}

    fake_detection = Detection(bbox=[0, 0, 5, 5], landmarks={}, score=0.9)
    fake_identity = Recognition(person="Test", similarity=0.9, embedding_norm=1.0)
    fake_emotion = Emotion(
        label="happy",
        probabilities={
            "neutral": 0.0,
            "happy": 1.0,
            "sad": 0.0,
            "angry": 0.0,
            "surprise": 0.0,
            "fear": 0.0,
            "disgust": 0.0,
        },
    )
    fake_result = PipelineResult(
        detections=[fake_detection],
        recognitions=[fake_identity],
        emotions=[fake_emotion],
        timings={"total": 1.0, "detect": 0.2},
    )

    class FakePipeline:
        def run(self, *_args, **_kwargs):  # noqa: ANN001
            return fake_result

    with patch("backend.dependencies.get_pipeline", return_value=FakePipeline()):
        response = client.post("/api/pipeline", json=image_payload)
    assert response.status_code == 200
    body = response.json()
    assert "faces" in body
    assert len(body["faces"]) == 1
    assert body["faces"][0]["identity"]["person"] == "Test"
