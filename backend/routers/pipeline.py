from __future__ import annotations

from fastapi import APIRouter, Body, Depends, File, UploadFile

from backend.dependencies import get_pipeline
from backend.routers.common import read_image_from_request
from backend.schemas.common import ImagePayload, PipelineOptions, PipelineResponse, PipelineFace, PipelineTiming

router = APIRouter(tags=["pipeline"])


@router.post("/pipeline", response_model=PipelineResponse)
async def run_pipeline(
    file: UploadFile | None = File(default=None),
    payload: ImagePayload | None = Body(default=None),
    options: PipelineOptions = Body(default=PipelineOptions()),
    pipeline=Depends(get_pipeline),
):
    image = await read_image_from_request(file, payload)
    result = pipeline.run(
        image,
        recognize=options.recognize,
        emotions=options.emotions,
        top_k=options.top_k or 3,
    )
    faces = []
    for detection, identity, emotion in zip(result.detections, result.recognitions, result.emotions):
        faces.append(
            PipelineFace(
                bbox=detection.bbox,
                landmarks=detection.landmarks,
                score=detection.score,
                identity=identity,
                emotion=emotion,
            )
        )
    timing = PipelineTiming(
        total=result.timings.get("total", 0.0),
        detect=result.timings.get("detect"),
        embed=result.timings.get("embed"),
        recognize=result.timings.get("recognize"),
        emotion=result.timings.get("emotion"),
    )
    return PipelineResponse(faces=faces, timing_ms=timing)
