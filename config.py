import os


class Config:
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
    OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), "output")
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
