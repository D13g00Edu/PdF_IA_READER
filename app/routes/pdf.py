from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid

from app.core.config import UPLOAD_DIR, MAX_FILE_SIZE
from app.services.rag_service import (
    load_pdf,
    split_pdf,
    create_vectorstore,
    set_vectorstore,
    save_vectorstore,
    save_metadata,
    build_metadata,
    clear_saved_index,
    load_metadata,
)
from app.schemas.pdf import UploadResponse


router = APIRouter()


@router.post("/upload-pdf", response_model=UploadResponse)
def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must have .pdf extension")

    file_bytes = file.file.read()

    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty file")

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")

    filename = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file_bytes)
    except Exception:
        raise HTTPException(status_code=500, detail="Error saving file")

    try:
        docs = load_pdf(file_path)
    except Exception:
        raise HTTPException(status_code=400, detail="Error reading PDF")

    if not docs:
        raise HTTPException(status_code=400, detail="PDF has no readable content")

    chunks = split_pdf(docs)
    if not chunks:
        raise HTTPException(status_code=400, detail="No chunks generated")

    try:
        clear_saved_index()
        vectorstore = create_vectorstore(chunks)
        set_vectorstore(vectorstore)
        save_vectorstore()

        metadata = build_metadata(
            original_filename=file.filename,
            stored_filename=filename,
            pages=len(docs),
            chunks=len(chunks)
        )
        save_metadata(metadata)
    except Exception:
        raise HTTPException(status_code=500, detail="Error creating persistent index")

    return {
        "message": "PDF uploaded and persisted",
        "metadata": load_metadata()
    }