import datetime
import hashlib
import random
from werkzeug.utils import secure_filename

import jwt
from flask import current_app

import boto3, botocore

s3 = boto3.client(
    "s3",
    aws_access_key_id="AWS_ACCESS_KEY",
    aws_secret_access_key="AWS_ACCESS_SECRET",
    region_name="us-east-1",
    # config=botocore.config.Config(signature_version="s3v4"),
)


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
def upload_profile_picture(file, user_id):
    filename = secure_filename(f"{user_id}_{file.filename}")
    s3_key = f"profile-pictures/{filename}"

    try:
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
        response = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": "profile-pictures-for-users", "Key": url},
            ExpiresIn=expiration,
        )
        return response
    except Exception as exception:
        print(exception)
        return exception
