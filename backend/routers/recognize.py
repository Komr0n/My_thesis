from __future__ import annotations

from typing import List

import numpy as np
from fastapi import APIRouter, Body, Depends, UploadFile, File

from backend.dependencies import get_detector, get_embedder, get_storage
from backend.routers.common import read_image_from_request
from backend.schemas.common import FaceDetection, Identity, ImagePayload, RecognizeOptions
from backend.utils.postprocessing import Detection
from backend.utils.preprocessing import align_face

router = APIRouter(tags=["recognition"])


@router.post("/recognize")
async def recognize_faces(
    file: UploadFile | None = File(default=None),
    payload: ImagePayload | None = Body(default=None),
    options: RecognizeOptions = Body(default=RecognizeOptions()),
    detector=Depends(get_detector),
    embedder=Depends(get_embedder),
    store=Depends(get_storage),
):
    image = await read_image_from_request(file, payload)
    detections = detector.detect(image)
    crops = []
    for detection in detections:
        x, y, w, h = map(int, detection.bbox)
        crop = image[y : y + h, x : x + w]
        crop = align_face({k: tuple(v) for k, v in detection.landmarks.items() if v}, crop)
        crops.append(crop)
    embeddings = embedder.embed(crops) if crops else []
    results = []
    for detection, embedding in zip(detections, embeddings):
        matches = store.topk_similar(embedding, top_k=options.top_k or 3)
        if matches:
            best = matches[0]
            identity = Identity(person=best.person, similarity=best.similarity, embedding_norm=best.embedding_norm)
        else:
            identity = Identity(person="Unknown", similarity=0.0, embedding_norm=float(np.linalg.norm(embedding)))
        results.append(
            {
                "person": identity.person,
                "similarity": identity.similarity,
                "embedding_norm": identity.embedding_norm,
                "bbox": detection.bbox,
                "score": detection.score,
            }
        )
    return results
