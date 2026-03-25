# 📄 PDF AI Reader

API construida con FastAPI que permite **subir PDFs y hacer preguntas sobre su contenido** utilizando **RAG (Retrieval-Augmented Generation)** y embeddings con Google Gemini.

---

## 🚀 ¿Qué hace este proyecto?

* 📤 Subes un PDF
* 🧠 Procesa el contenido en fragmentos (chunks)
* 🔢 Convierte el texto en embeddings
* ⚡ Indexa la información con FAISS
* 💬 Permite hacer preguntas y responder con contexto del documento

---

## 🧱 Arquitectura del proyecto

```
app/
│
├── main.py                # Inicializa FastAPI
├── routes/
│   ├── pdf.py             # Endpoints para manejo de PDFs
│   └── chat.py            # Endpoint para preguntas (RAG)
│
├── services/
│   └── rag_service.py     # Lógica de embeddings, FAISS y generación de respuestas
│
├── core/
│   └── config.py          # Configuración y variables de entorno
│
storage/
├── uploads/               # PDFs subidos
├── vectordb/              # Índice FAISS
└── metadata.json          # Metadatos
```

---

## ⚙️ Requisitos

* Python 3.10 o superior
* Entorno virtual

### Instalación

```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

Si no tienes `requirements.txt`, instala:

```bash
pip install fastapi uvicorn langchain langchain-google-genai langchain-community faiss-cpu
```
---

## ▶️ Ejecutar el proyecto

```bash
uvicorn app.main:app --reload
```

Abrir documentación interactiva:

👉 http://127.0.0.1:8000/docs

---

## 🔌 Endpoints principales

### 📤 Subir PDF

```
POST /pdf/upload
```

* Guarda el archivo
* Procesa embeddings
* Crea índice FAISS

---

### ❓ Hacer preguntas

```
POST /chat/ask
```

Body:

```json
{
  "question": "¿De qué trata el documento?"
}
```

* Busca contenido relevante
* Responde usando contexto del PDF

---

### 🧹 Limpiar datos

```
POST /pdf/clear
```

* Elimina archivos, índice y metadata

---

## 🧠 ¿Cómo funciona internamente?

1. Se carga el PDF
2. Se divide en fragmentos (chunks)
3. Se generan embeddings (vectores)
4. Se almacenan en FAISS
5. Al preguntar:

   * Se busca el contenido más similar
   * Se genera una respuesta basada en ese contexto

---

## 🔒 Buenas prácticas antes de subir a GitHub

* ❌ No incluir API keys en el código
* ✅ Usar variables de entorno
* ✅ Verificar `.gitignore`:

```
venv/
.env
storage/
```

---

## 🧪 Prueba rápida

1. Inicia el servidor
2. Ve a `/docs`
3. Usa `/pdf/upload` para subir un archivo
4. Usa `/chat/ask` para hacer preguntas
5. Verifica que responde correctamente

---

## 📌 Notas

* El modelo responde **solo con la información del PDF**
* Si no encuentra contexto, la respuesta puede ser limitada
* Ideal para documentos largos o análisis de contenido

---

## 💡 Futuras mejoras

* Control de tamaño de archivos
* Autenticación (JWT)
* Ajuste dinámico de `k` en búsqueda
* Endpoint de estado (`/healthz`)
* Soporte multi-documento

---

## 📚 Tecnologías usadas

* FastAPI
* LangChain
* Google Generative AI (Gemini)
* FAISS
* Python

---

## 🧾 Licencia

Uso libre para fines educativos y desarrollo.
