import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    POPPLER_PATH = os.getenv("POPPLER_PATH", "/usr/bin")
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_FILE_SIZE_MB = "10"
    ALLOWED_MIME_TYPES = [
        "image/jpeg",
        "image/png",
        "application/pdf"
    ]
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    IMAGE_OUTPUT_FORMAT = "JPEG"
    IMAGE_QUALITY = 85  # For JPEG compression
    PDF_CONVERSION_FMT = "jpeg"  # Match file_handler.py