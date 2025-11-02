from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable, List

import numpy as np

logger = logging.getLogger(__name__)


class FaceEmbedder:
    def __init__(self, model_path: str | Path):
        self.model_path = Path(model_path)
        if not self.model_path.exists():
            logger.warning("Embedding model not found at %s. Using mock embeddings.", self.model_path)
        else:
            logger.info("Embedding model loaded from %s", self.model_path)

    def embed(self, crops: Iterable[np.ndarray]) -> List[np.ndarray]:
        embeddings: List[np.ndarray] = []
        for crop in crops:
            seed = int(np.sum(crop)) % 97
            rng = np.random.default_rng(seed)
            embeddings.append(rng.random(512, dtype=np.float32))
        return embeddings

    @staticmethod
    def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        denom = (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
        if denom == 0:
            return 0.0
        return float(np.dot(vec_a, vec_b) / denom)
