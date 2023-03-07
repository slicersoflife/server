import os


class BaseConfig:
    """Base configuration."""

    DATABASE_URL = os.getenv("DATABASE_URL")
    PORT = os.getenv("PORT", "8080")
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = "Content-Type"
