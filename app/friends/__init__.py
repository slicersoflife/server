from flask import Blueprint
from .routes import add_routes

friends = Blueprint("friends", __name__)
add_routes(friends)
