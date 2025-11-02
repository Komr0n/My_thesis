from __future__ import annotations

import numpy as np
from fastapi import APIRouter, Depends, HTTPException

from backend.dependencies import get_detector, get_embedder, get_storage
from backend.schemas.common import EnrollRequest, EnrollResponse
from backend.utils.preprocessing import align_face, image_from_base64

router = APIRouter(tags=["enroll"])


@router.post("/enroll", response_model=EnrollResponse)
async def enroll_person(
    request: EnrollRequest,
    detector=Depends(get_detector),
    embedder=Depends(get_embedder),
    store=Depends(get_storage),
) -> EnrollResponse:
    if not request.images:
        raise HTTPException(status_code=400, detail="At least one image is required")

    embeddings: list[np.ndarray] = []
    for encoded in request.images:
        try:
            image = image_from_base64(encoded)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        detections = detector.detect(image)
        if not detections:
            continue
        detection = detections[0]
        x, y, w, h = map(int, detection.bbox)
        crop = image[y : y + h, x : x + w]
        crop = align_face({k: tuple(v) for k, v in detection.landmarks.items() if v}, crop)
        embedding = embedder.embed([crop])[0]
        embeddings.append(embedding)

    if not embeddings:
        raise HTTPException(status_code=422, detail="No faces detected in provided images")

    averaged = np.mean(embeddings, axis=0)
    person = store.add_person(request.name, [averaged], notes=request.notes)
    return EnrollResponse(person_id=person.id, name=person.name, samples=len(embeddings))
