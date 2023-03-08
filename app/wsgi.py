import os

from dotenv import load_dotenv
from flask import Flask

from app.auth import auth as auth_blueprint
from app.extensions import db, migrate


def load_app() -> Flask:
    load_dotenv()

    main_app = Flask(__name__)
    main_app.config.from_object(f'app.config.{os.getenv("CONFIG", "BaseConfig")}')
    main_app.register_blueprint(auth_blueprint)

    db.init_app(main_app)
    migrate.init_app(main_app, db)

    with main_app.app_context():
        db.create_all()
        print("Connected to database.")

    return main_app


if __name__ == "__main__":
    app = load_app()
    app.run(app.config.get("PORT"))
