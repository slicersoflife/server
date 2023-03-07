from flask import Blueprint
from .routes import add_routes

auth = Blueprint("auth", __name__)
add_routes(auth)
