import os
import datetime
import hashlib
import random
from werkzeug.utils import secure_filename

import jwt
from flask import current_app
from flask import request, jsonify, Blueprint, current_app
from app.extensions import s3

import boto3, botocore


### AUTH ###
def encode_token(identifier):
    try:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=60),
            "iat": datetime.datetime.utcnow(),
            "sub": str(identifier),
        }
        return jwt.encode(
            payload, current_app.config.get("SECRET_KEY"), algorithm="HS256"
        )
    except Exception as exception:
        return exception


def decode_token(token):
    payload = jwt.decode(
        token, current_app.config.get("SECRET_KEY"), algorithms="HS256"
    )
    return payload.get("sub")


def get_hash(phone):
    return hashlib.sha256(phone.encode("utf-8")).hexdigest()


def generate_code():
    return "".join(
        random.choices(
            list(map(str, range(9))),
            k=current_app.config.get("VERIFICATION_CODE_LENGTH"),
        ),
    )


### S3 ###
def upload_profile(file, user_id):
    filename = secure_filename(f"{user_id}_{file.filename}")
    s3_key = f"profile-pictures/{filename}"

    try:
        print("Uploading profile picture to s3")
        s3.upload_fileobj(
            file,
            "profile-pictures-for-users",
            s3_key,
            ExtraArgs={"ACL": "public-read", "ContentType": file.content_type},
        )
        return f"https://profile-pictures-for-users.s3.amazonaws.com/{s3_key}"
    except Exception as exception:
        print(exception)
        return exception


def get_presigned_url(url, expiration):
    try:
        print("Generating presigned url")
        response = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": "profile-pictures-for-users", "Key": url},
            ExpiresIn=expiration,
        )
        return response
    except Exception as exception:
        print(exception)
        return exception
