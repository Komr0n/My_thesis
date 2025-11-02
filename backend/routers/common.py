from __future__ import annotations

from fastapi import HTTPException, UploadFile

from backend.schemas.common import ImagePayload
from backend.utils.preprocessing import decode_image, image_from_base64


async def read_image_from_request(
    file: UploadFile | None,
    payload: ImagePayload | None,
):
    if file is not None:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        return decode_image(content)
    if payload is not None:
        try:
            return image_from_base64(payload.image_base64)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
    raise HTTPException(status_code=400, detail="Image file or base64 payload required")
