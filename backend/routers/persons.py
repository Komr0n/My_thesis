from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from backend.dependencies import get_storage
from backend.schemas.common import DeleteResponse, PersonsResponse

router = APIRouter(tags=["persons"])


@router.get("/persons", response_model=PersonsResponse)
def list_persons(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    storage=Depends(get_storage),
) -> PersonsResponse:
    results, total = storage.list_persons(limit=limit, offset=offset)
    return PersonsResponse(results=results, total=total)


@router.delete("/persons/{person_id}", response_model=DeleteResponse)
def delete_person(person_id: int, storage=Depends(get_storage)) -> DeleteResponse:
    deleted = storage.delete_person(person_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Person not found")
    return DeleteResponse(deleted=True)
