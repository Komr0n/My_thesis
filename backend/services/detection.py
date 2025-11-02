from __future__ import annotations

import logging
from pathlib import Path
from typing import List

import numpy as np

from backend.utils.postprocessing import Detection

logger = logging.getLogger(__name__)


class FaceDetector:
    def __init__(self, model_path: str | Path):
        self.model_path = Path(model_path)
        if not self.model_path.exists():
            logger.warning("Detection model not found at %s. Using mock detections.", self.model_path)
        else:
            logger.info("Detection model loaded from %s", self.model_path)

    def detect(self, image: np.ndarray) -> List[Detection]:
        # Placeholder detection returning empty list.
        logger.debug("Running mock detection on image with shape %s", image.shape)
        return []
