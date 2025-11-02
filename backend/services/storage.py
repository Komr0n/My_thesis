from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable, List, Sequence

import numpy as np
from sqlalchemy import func, select

from backend.db import models
from backend.db.database import SessionLocal
from backend.schemas.common import PersonRecord

logger = logging.getLogger(__name__)


@dataclass
class SimilarPerson:
    person: str
    similarity: float
    embedding_norm: float


class EmbeddingStore:
    def __init__(self, threshold: float = 0.6) -> None:
        self.threshold = threshold

    def add_person(self, name: str, embeddings: Sequence[np.ndarray], notes: str | None = None) -> models.Person:
        with SessionLocal() as session:
            person = models.Person(name=name, notes=notes)
            session.add(person)
            session.flush()
            for vector in embeddings:
                session.add(
                    models.Embedding(
                        person_id=person.id,
                        vector=vector.astype(np.float32).tobytes(),
                        metadata="{}",
                    )
                )
            session.commit()
            session.refresh(person)
            logger.info("Added person %s with %d embeddings", name, len(embeddings))
            return person

    def delete_person(self, person_id: int) -> bool:
        with SessionLocal() as session:
            person = session.get(models.Person, person_id)
            if not person:
                return False
            session.delete(person)
            session.commit()
            return True

    def list_persons(self, limit: int = 50, offset: int = 0) -> tuple[list[PersonRecord], int]:
        with SessionLocal() as session:
            total = session.scalar(select(func.count(models.Person.id))) or 0
            persons = session.execute(
                select(models.Person).order_by(models.Person.created_at.desc()).offset(offset).limit(limit)
            ).scalars()
            results = [
                PersonRecord(
                    id=person.id,
                    name=person.name,
                    notes=person.notes,
                    embedding_count=len(person.embeddings),
                )
                for person in persons
            ]
            return results, int(total)

    def topk_similar(self, embedding: np.ndarray, top_k: int = 3) -> list[SimilarPerson]:
        with SessionLocal() as session:
            embeddings = session.execute(select(models.Embedding).join(models.Person)).scalars().all()
            scored: list[SimilarPerson] = []
            norm = float(np.linalg.norm(embedding)) or 1.0
            for entry in embeddings:
                vector = np.frombuffer(entry.vector, dtype=np.float32)
                denom = (float(np.linalg.norm(vector)) * norm) or 1.0
                similarity = float(np.dot(vector, embedding) / denom)
                if similarity >= self.threshold:
                    scored.append(
                        SimilarPerson(
                            person=entry.person.name,
                            similarity=similarity,
                            embedding_norm=float(np.linalg.norm(vector)),
                        )
                    )
            scored.sort(key=lambda x: x.similarity, reverse=True)
            return scored[:top_k]
