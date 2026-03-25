# PDF AI Reader

Proyecto FastAPI para cargar PDF y responder preguntas usando embeddings + RAG (Google Gemini).

## Estructura

- `app/main.py`: app FastAPI
- `app/routes/*`: rutas `chat` y `pdf`
- `app/services/rag_service.py`: pipeline de embeddings, vector store y respuestas con Gemini
- `app/core/config.py`: configuración de rutas y env
- `storage/`: archivos subidos, vector db y metadata

## Requisitos

- Python 3.11+ (o 3.10)
- Crear un virtualenv, activar e instalar dependencias:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

> Si no tienes `requirements.txt`, instala:
> `fastapi`, `uvicorn`, `langchain`, `langchain-google-genai`, `langchain-community`, `faiss-cpu`, etc.

## Variables de entorno (obligatorio)

No debe haber credenciales en el código. Se usa:

- `GOOGLE_API_KEY` (tu clave GEMINI/Google Generative AI)

Ejemplo local:

```bash
set GOOGLE_API_KEY=tu_clave_aqui
```

O archivo `.env` (no subido a git gracias a `.gitignore`):

```
GOOGLE_API_KEY=tu_clave_aqui
```

## Puesta en marcha

```bash
uvicorn app.main:app --reload
```

- Abre `http://127.0.0.1:8000/docs`

## Limpieza y seguridad antes de push a GitHub

1. Confirmar que no hay claves en los archivos fuente (`app/services/rag_service.py` ahora usa `GOOGLE_API_KEY`).
2. Añadir `.gitignore` y asegurar `storage/`, `venv/`, `.env` están ignorados.
3. Revisión rápida:
   - `git status`
   - `git diff` (no aparece la API key)
4. Commit y push:
   - `git add .`
   - `git commit -m "Inicial: setup PDF AI Reader con env seguro"`
   - `git push origin main`

## Nota

Si en algún lugar aún hay un token hardcodeado, eliminarlo e inevitablemente usar `os.getenv("GOOGLE_API_KEY")`, como ya está en `app/services/rag_service.py` y `app/core/config.py`.
