from uuid import uuid4 as uuid

from flask import request, jsonify, Blueprint, current_app
from flask_cors import cross_origin
from sqlalchemy import select

from app.extensions import db, cache, twilio
from .helpers import encode_auth_token, generate_code, get_hash
from .models import User


def add_routes(bp: Blueprint):
    @bp.post("/register")
    @cross_origin()
    def register():
        post_data = request.get_json()

        if "phone" not in post_data:
            response_object = {
                "status": "fail",
                "message": "You must provide a phone number.",
            }
            return jsonify(response_object), 401

        user = db.session.execute(
            select(User).filter_by(phone=post_data.get("phone"))
        ).first()
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
                phone=get_hash(post_data.get("phone")),
            )
            db.session.add(user)
            db.session.commit()

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
            return jsonify(response_object), 503

    @bp.post("/verify/start")
    @cross_origin()
    def verify_start():
        post_data = request.get_json()

        if "phone" not in post_data:
            response_object = {
                "status": "fail",
                "message": "You must provide a phone number.",
            }
            return jsonify(response_object), 401

        try:
            phone_number_hash = get_hash(post_data.get("phone"))
            code = generate_code()
            cache.set(
                phone_number_hash,
                code,
                ex=current_app.config.get("VERIFICATION_CODE_TTL"),
            )
            twilio.messages.create(
                from_=current_app.config.get("TWILIO_PHONE_NUMBER"),
                to=post_data.get("phone"),
                body=f"{code} is your verification code for Slice of Life.",
            )
            response_object = {"status": "success", "message": "Sent verification."}
            return jsonify(response_object), 200

        except Exception as exception:
            print(exception)
            response_object = {"status": "fail", "message": str(exception)}
            return jsonify(response_object), 503

    @bp.post("/verify")
    def verify():
        post_data = request.get_json()
        if "phone" not in post_data or "code" not in post_data:
            response_object = {
                "status": "fail",
                "message": "You must provide a phone number and verification code.",
            }
            return jsonify(response_object), 401

        phone_number_hash = get_hash(post_data.get("phone"))
        saved_code = cache.get(phone_number_hash)

        if saved_code is None:
            response_object = {
                "status": "fail",
                "message": "That phone number is unknown.",
            }
            return jsonify(response_object), 401

        if saved_code != post_data.get("code"):
            response_object = {
                "status": "fail",
                "message": "Wrong verification code.",
            }
            return jsonify(response_object), 401

        response_object = {
            "status": "success",
            "message": "Correct verification code.",
        }
        return jsonify(response_object), 200
