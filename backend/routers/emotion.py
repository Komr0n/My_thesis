from __future__ import annotations

from typing import List

from fastapi import APIRouter, Body, Depends, File, UploadFile

from backend.dependencies import get_detector, get_emotion_model
from backend.routers.common import read_image_from_request
from backend.schemas.common import EmotionResponse, ImagePayload
from backend.utils.postprocessing import Emotion
from backend.utils.preprocessing import align_face

router = APIRouter(tags=["emotion"])


@router.post("/emotion", response_model=List[EmotionResponse])
async def emotion_from_image(
    file: UploadFile | None = File(default=None),
    payload: ImagePayload | None = Body(default=None),
    detector=Depends(get_detector),
    emotion_model=Depends(get_emotion_model),
):
    image = await read_image_from_request(file, payload)
    detections = detector.detect(image)
    crops = []
    for detection in detections:
        x, y, w, h = map(int, detection.bbox)
        crop = image[y : y + h, x : x + w]
        crop = align_face({k: tuple(v) for k, v in detection.landmarks.items() if v}, crop)
        crops.append(crop)
    emotions = emotion_model.classify(crops) if crops else []
    responses: List[EmotionResponse] = []
    for detection, emotion in zip(detections, emotions):
        responses.append(
            EmotionResponse(
                emotion=emotion.label,
                probabilities=emotion.probabilities,
                bbox=detection.bbox,
            )
        )
    return responses
