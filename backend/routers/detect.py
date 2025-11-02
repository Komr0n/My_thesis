from __future__ import annotations

from typing import List

from fastapi import APIRouter, Body, Depends, UploadFile, File

from backend.dependencies import get_detector
from backend.routers.common import read_image_from_request
from backend.schemas.common import FaceDetection, ImagePayload
from backend.utils.postprocessing import Detection

router = APIRouter(tags=["detection"])


@router.post("/detect", response_model=List[FaceDetection])
async def detect_faces(
    file: UploadFile | None = File(default=None),
    payload: ImagePayload | None = Body(default=None),
    detector=Depends(get_detector),
) -> List[FaceDetection]:
    image = await read_image_from_request(file, payload)
    detections = detector.detect(image)
    response: List[FaceDetection] = []
    for idx, detection in enumerate(detections):
        response.append(
            FaceDetection(
                id=idx,
                bbox=detection.bbox,
                landmarks=detection.landmarks,
                score=detection.score,
            )
        )
    return response
