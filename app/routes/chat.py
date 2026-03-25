from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.schemas.chat import AskRequest, AskResponse
from app.services.rag_service import (
    get_vectorstore,
    search_similar_chunks,
    answer_with_context,
    load_metadata,
)

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
def ask_question(data: AskRequest):
    vectorstore = get_vectorstore()

    if vectorstore is None:
        raise HTTPException(status_code=400, detail="No PDF uploaded yet")

    if not data.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    chunks = search_similar_chunks(data.question, k=1)

    if not chunks:
        return {
            "question": data.question,
            "answer": "No encontré información relevante en el PDF.",
            "sources": [],
            "chunks_used": []
        }

    answer = answer_with_context(data.question, chunks)
    metadata = load_metadata()

    return {
        "question": data.question,
        "answer": answer,
        "document": metadata,
        "sources": [
            {
                "source": doc.metadata.get("source"),
                "page": doc.metadata.get("page", 0) + 1
            }
            for doc in chunks
        ],
        "chunks_used": [
            {
                "content_preview": doc.page_content[:200],
                "page": doc.metadata.get("page", 0) + 1
            }
            for doc in chunks
        ]
    }