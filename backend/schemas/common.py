from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field, root_validator

EMOTION_LABELS = ["neutral", "happy", "sad", "angry", "surprise", "fear", "disgust"]


class HealthResponse(BaseModel):
    status: str
    version: str


class LandmarkSet(BaseModel):
    l_eye: List[float] | None = None
    r_eye: List[float] | None = None
    nose: List[float] | None = None
    l_mouth: List[float] | None = None
    r_mouth: List[float] | None = None


class FaceDetection(BaseModel):
    id: int | None = None
    bbox: List[float]
    landmarks: LandmarkSet
    score: float


class Identity(BaseModel):
    person: str
    similarity: float
    embedding_norm: float | None = None


class EmotionProbabilities(BaseModel):
    neutral: float
    happy: float
    sad: float
    angry: float
    surprise: float
    fear: float
    disgust: float


class EmotionResponse(BaseModel):
    emotion: str
    probabilities: EmotionProbabilities
    bbox: List[float] | None = None


class PipelineFace(BaseModel):
    bbox: List[float]
    landmarks: LandmarkSet
    score: float
    identity: Identity | None = None
    emotion: EmotionResponse | None = None


class PipelineTiming(BaseModel):
    total: float
    detect: float | None = None
    embed: float | None = None
    recognize: float | None = None
    emotion: float | None = None


class PipelineResponse(BaseModel):
    faces: List[PipelineFace]
    timing_ms: PipelineTiming


class ImagePayload(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded image")


class RecognizeOptions(BaseModel):
    top_k: int | None = Field(default=3, ge=1, le=10)
    threshold: float | None = Field(default=0.6, ge=0.0, le=1.0)


class PipelineOptions(RecognizeOptions):
    recognize: bool = True
    emotions: bool = True


class PipelineRequest(BaseModel):
    payload: ImagePayload | None = None
    options: PipelineOptions = Field(default_factory=PipelineOptions)

    @root_validator(pre=True)
    def flatten_body(cls, values: dict | None) -> dict:
        if values is None:
            return {}
        if not isinstance(values, dict):
            return values

        data = dict(values)

        if "payload" not in data and "image_base64" in data:
            image_base64 = data.pop("image_base64")
            data["payload"] = {"image_base64": image_base64}

        if "options" not in data:
            option_keys = {"recognize", "emotions", "top_k", "threshold"}
            option_values = {
                key: data.pop(key)
                for key in list(data.keys())
                if key in option_keys
            }
            if option_values:
                data["options"] = option_values

        return data


class EnrollRequest(BaseModel):
    name: str
    images: List[str]
    notes: str | None = None


class EnrollResponse(BaseModel):
    person_id: int
    name: str
    samples: int


class PersonRecord(BaseModel):
    id: int
    name: str
    notes: str | None = None
    embedding_count: int


class PersonsResponse(BaseModel):
    results: List[PersonRecord]
    total: int


class DeleteResponse(BaseModel):
    deleted: bool
