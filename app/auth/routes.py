import datetime
from uuid import uuid4 as uuid

import jwt
from flask import request, jsonify, current_app, Blueprint
from flask_cors import cross_origin

from app.extensions import Session
from .models import User


def encode_auth_token(user_id):
    try:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=60),
            "iat": datetime.datetime.utcnow(),
            "sub": str(user_id),
        }
        return jwt.encode(
            payload, current_app.config.get("SECRET_KEY"), algorithm="HS256"
        )
    except Exception as exception:
        return exception


def add_routes(bp: Blueprint):
    @bp.post("/register")
    @cross_origin()
    def register():
        session = Session()

        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = session.query(User).filter_by(phone=post_data.get("phone")).first()
        if user:
            response_object = {
                "status": "fail",
                "message": "User already exists. Please log in.",
            }
            return jsonify(response_object), 202

        try:
            # TODO: Verify phone number
            # TODO: Phone number encryption
            user = User(
                id=uuid(),
                display_name=post_data.get("display_name"),
                username=post_data.get("username"),
                phone=post_data.get("phone"),
            )
            session.add(user)
            session.commit()

            # generate the auth token
            auth_token = encode_auth_token(user.id)
            response_object = {
                "status": "success",
                "message": "Successfully registered.",
                "auth_token": auth_token,
            }
            return jsonify(response_object), 201

        except Exception as exception:
            print(exception)
            response_object = {
                "status": "fail",
                "message": "Some error occurred. Please try again.",
            }
            return jsonify(response_object), 401

    @bp.post("/login")
    @cross_origin()
    def login():
        session = Session()

        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = session.query(User).filter_by(email=post_data.get("phone")).first()
            if not user:
                response_object = {"status": "fail", "message": "User does not exist."}
                return jsonify(response_object), 404

            # TODO: Verify phone number

            auth_token = encode_auth_token(user.id)
            response_object = {
                "status": "success",
                "message": "Successfully logged in.",
                "auth_token": auth_token,
            }
            return jsonify(response_object), 200

        except Exception as exception:
            print(exception)
            response_object = {"status": "fail", "message": str(exception)}
            return jsonify(response_object), 500
