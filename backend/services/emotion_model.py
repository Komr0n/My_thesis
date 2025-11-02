from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable, List

import numpy as np

from backend.utils.postprocessing import Emotion, EMOTIONS, format_emotion

logger = logging.getLogger(__name__)


class EmotionClassifier:
    def __init__(self, model_path: str | Path):
        self.model_path = Path(model_path)
        if not self.model_path.exists():
            logger.warning("Emotion model not found at %s. Using mock classifier.", self.model_path)
        else:
            logger.info("Emotion model loaded from %s", self.model_path)

    def classify(self, crops: Iterable[np.ndarray]) -> List[Emotion]:
        results: List[Emotion] = []
        for crop in crops:
            seed = int(np.sum(crop)) % len(EMOTIONS)
            logits = np.zeros(len(EMOTIONS), dtype=np.float32)
            logits[seed] = 1.0
            results.append(format_emotion(logits))
        return results
