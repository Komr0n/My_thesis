from __future__ import annotations

import base64
import io
from typing import Optional

import cv2
import numpy as np


def decode_image(data: bytes) -> np.ndarray:
    array = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Unable to decode image bytes")
    return image


def image_from_base64(data: str) -> np.ndarray:
    if "," in data:
        data = data.split(",", 1)[1]
    try:
        binary = base64.b64decode(data)
    except (ValueError, base64.binascii.Error) as exc:
        raise ValueError("Invalid base64 image payload") from exc
    return decode_image(binary)


def align_face(landmarks: dict[str, tuple[float, float]], image: np.ndarray) -> np.ndarray:
    # Placeholder alignment using eye landmarks; in production use similarity transform
    left_eye = landmarks.get("l_eye")
    right_eye = landmarks.get("r_eye")
    if not left_eye or not right_eye:
        return image
    # compute simple rotation
    eye_delta = np.subtract(right_eye, left_eye)
    angle = np.degrees(np.arctan2(eye_delta[1], eye_delta[0]))
    center = tuple(np.mean([left_eye, right_eye], axis=0))
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    aligned = cv2.warpAffine(image, matrix, (image.shape[1], image.shape[0]))
    return aligned


def resize_for_inference(image: np.ndarray, max_side: int = 640) -> tuple[np.ndarray, float]:
    h, w = image.shape[:2]
    scale = 1.0
    if max(h, w) > max_side:
        scale = max_side / max(h, w)
        image = cv2.resize(image, (int(w * scale), int(h * scale)))
    return image, scale


def to_jpeg_bytes(image: np.ndarray, quality: int = 90) -> bytes:
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    success, encoded = cv2.imencode(".jpg", image, encode_param)
    if not success:
        raise ValueError("Failed to encode image to JPEG")
    return encoded.tobytes()
