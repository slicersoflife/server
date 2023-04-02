from pprint import pprint
from sqlalchemy import select

from app.auth.models import User
from app.auth.schema import user_schema
from app.extensions import db
from app.wsgi import load_app

app = load_app()
with app.app_context():
    user = db.session.scalars(select(User).where(User.username == "saptarshi8")).first()
    pprint(user_schema.dump(user))
