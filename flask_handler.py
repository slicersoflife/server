import os

from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import create_engine

from auth import auth as auth_blueprint
from extensions import Session
from models import Base


def load_app() -> Flask:
    load_dotenv()

    main_app = Flask(__name__)
    main_app.config.from_object(f'config.{os.getenv("CONFIG", "BaseConfig")}')
    main_app.register_blueprint(auth_blueprint)

    engine = create_engine(main_app.config.get('DATABASE_URL'))
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)
    print("Connected to database.")

    return main_app


if __name__ == "__main__":
    app = load_app()
    app.run(app.config.get('PORT'))
