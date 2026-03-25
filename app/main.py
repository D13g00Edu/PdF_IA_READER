from fastapi import FastAPI

from app.routes import pdf, chat
from app.services.rag_service import load_vectorstore_from_disk

app = FastAPI()

app.include_router(pdf.router)
app.include_router(chat.router)


@app.on_event("startup")
def startup_event():
    load_vectorstore_from_disk()


@app.get("/health")
def health():
    return {"status": "ok"}