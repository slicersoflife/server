from uuid import uuid4 as uuid

from flask import request, jsonify, Blueprint, current_app
from sqlalchemy import select

from app.extensions import db, cache, twilio, s3
from .helpers import (
    encode_token,
    decode_token,
    generate_code,
    get_hash,
    upload_profile,
    get_presigned_url,
)
from .models import User
from .schema import user_schema


def add_routes(bp: Blueprint):
    ## AUTHENTICATION
    @bp.post("/verify/start/mock")
    def verify_start_mock():
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
            response_object = {
                "status": "success",
                "message": f"{code} is your verification code for Slice of Life.",
            }
            return jsonify(response_object), 200

        except Exception as exception:
            print(exception)
            response_object = {"status": "fail", "message": str(exception)}
            return jsonify(response_object), 503

    @bp.post("/verify/start")
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

        try:
            user = db.session.scalars(
                select(User).filter_by(phone=phone_number_hash)
            ).first()
            if user is None:
                verification_token = encode_token(phone_number_hash)
                response_object = {
                    "status": "verified",
                    "message": "Correct verification code.",
                    "verification_token": verification_token,
                }
                return jsonify(response_object), 200
            else:
                auth_token = encode_token(user.id)
                response_object = {
                    "status": "authenticated",
                    "message": "Successfully logged in.",
                    "auth_token": auth_token,
                    "user": user_schema.dump(user),
                }
                return jsonify(response_object), 201

        except Exception as exception:
            print(exception)
            response_object = {
                "status": "fail",
                "message": "Some error occurred. Please try again.",
            }
            return jsonify(response_object), 503

    @bp.post("/register")
    def register():
        post_data = request.get_json()

        if "Authorization" not in request.headers:
            response_object = {
                "status": "fail",
                "message": "You must provide a verification token.",
            }
            return jsonify(response_object), 401

        auth_header = request.headers.get("Authorization").split()
        if len(auth_header) < 2:
            response_object = {
                "status": "fail",
                "message": "Invalid authorization header format.",
            }
            return jsonify(response_object), 401

        phone_number_hash = decode_token(auth_header[1])
        user = db.session.execute(
            select(User).filter_by(phone=phone_number_hash)
        ).first()
        if user:
            response_object = {
                "status": "fail",
                "message": "User already exists. Please log in.",
            }
            return jsonify(response_object), 202

        try:
            user = User(
                id=uuid(),
                display_name=post_data.get("display_name"),
                username=post_data.get("username"),
                phone=phone_number_hash,
            )
            db.session.add(user)
            db.session.commit()

            auth_token = encode_token(user.id)
            response_object = {
                "status": "success",
                "message": "Successfully registered.",
                "auth_token": auth_token,
                "user": user_schema.dump(user),
            }
            return jsonify(response_object), 201

        except Exception as exception:
            print(exception)
            response_object = {
                "status": "fail",
                "message": "Some error occurred. Please try again.",
            }
            return jsonify(response_object), 503

    ## Profile
    @bp.post("/profile/picture_upload")
    def upload_profile_picture():
        user_id = request.form.get("user_id")
        file = request.files.get("profile_picture")
        file.filename = user_id + ".png"
        if not file:
            response_object = {
                "status": "fail",
                "message": "No file found",
            }
            return jsonify(response_object), 401

        user = db.session.execute(select(User).filter_by(id=user_id)).first()

        if user is None:
            response_object = {
                "status": "fail",
                "message": "User not found",
            }
            return jsonify(response_object), 401

        profile_picture_url = upload_profile(file, user_id)

        db.session.query(User).filter(User.id == user_id).update(
            {"profile_picture_url": profile_picture_url}
        )
        db.session.commit()

        response_object = {
            "status": "success",
            "message": "Successfully uploaded profile picture",
        }
        return jsonify(response_object), 201

    @bp.post("/profile/get_picture")
    def get_profile_picture():
        user_id = request.form.get("user_id")

        profile_picture = db.session.execute(
            select(User.profile_picture_url).filter_by(id=user_id)
        ).first()

        if profile_picture is None:
            response_object = {
                "status": "fail",
                "message": "User not found",
            }
            return jsonify(response_object), 401

        profile_picture = str(profile_picture)

        response_object = {
            "status": "success",
            "message": "Successfully retrieved profile picture",
        }
        return profile_picture, 200
