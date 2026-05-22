import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the backend/ directory regardless of current working directory.
load_dotenv(Path(__file__).resolve().parent / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError(
            "DATABASE_URL is not set. Copy backend/.env.example to backend/.env "
            "and configure the database connection there."
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@plastinki.local")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
