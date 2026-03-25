from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., example="¿De qué trata el documento?")


class Source(BaseModel):
    source: str
    page: int


class ChunkPreview(BaseModel):
    content_preview: str
    page: int


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]
    chunks_used: list[ChunkPreview]