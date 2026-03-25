import os

BASE_DIR = "storage"
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
VECTORDB_DIR = os.path.join(BASE_DIR, "vectordb")
METADATA_PATH = os.path.join(BASE_DIR, "metadata.json")

# Use environment variable for API key to avoid hardcoding credentials
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(VECTORDB_DIR, exist_ok=True)