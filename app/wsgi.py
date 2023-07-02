import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from app.extensions import db, migrate
from app.auth import auth as auth_blueprint
from app.friends import friends as friends_blueprint


def load_app() -> Flask:
    load_dotenv()

    main_app = Flask(__name__)
    main_app.config.from_object(f'app.config.{os.getenv("CONFIG", "BaseConfig")}')
    main_app.register_blueprint(auth_blueprint)
    main_app.register_blueprint(friends_blueprint)

    main_app.config["S3_BUCKET"] = "S3_BUCKET_NAME"
    main_app.config["S3_KEY"] = "AWS_ACCESS_KEY"
    main_app.config["S3_SECRET"] = "AWS_ACCESS_SECRET"

    CORS(main_app, origins="*")
    db.init_app(main_app)
    migrate.init_app(main_app, db)

    with main_app.app_context():
        db.create_all()
        print("Connected to database.")

    return main_app


if __name__ == "__main__":
    app = load_app()
    app.run(app.config.get("PORT"))
