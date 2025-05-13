# Aggiungi in un file `models.py`
from pydantic import BaseModel

class Entity(BaseModel):
    text: str
    label: str

class Chunk(BaseModel):
    chunk_id: int
    text: str
    source: str
    start_time: float | None = None
    end_time: float | None = None
    entities: list[Entity] = []

class RagResponse(BaseModel):
    testoRisp: str | None = None
    chunks: list[Chunk] = []