from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

import numpy as np


@dataclass
class Detection:
    bbox: list[float]
    landmarks: dict[str, list[float]]
    score: float


@dataclass
class Recognition:
    person: str
    similarity: float
    embedding_norm: float


@dataclass
class Emotion:
    label: str
    probabilities: dict[str, float]


EMOTIONS = ["neutral", "happy", "sad", "angry", "surprise", "fear", "disgust"]


def softmax(logits: Iterable[float]) -> list[float]:
    logits_array = np.array(list(logits), dtype=np.float32)
    exp = np.exp(logits_array - np.max(logits_array))
    probs = exp / np.sum(exp)
    return probs.tolist()


def format_emotion(probabilities: Iterable[float]) -> Emotion:
    probs = softmax(probabilities)
    mapping = {label: float(prob) for label, prob in zip(EMOTIONS, probs)}
    label = max(mapping, key=mapping.get)
    return Emotion(label=label, probabilities=mapping)
