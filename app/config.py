import os


class BaseConfig:
    """Base configuration."""

    PORT = os.getenv("PORT", "8080")
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    CORS_HEADERS = "Content-Type"
