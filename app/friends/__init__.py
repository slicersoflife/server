from flask import Blueprint
from .routes import add_routes

auth = Blueprint("friends", __name__)
add_routes(friends)
