import datetime
import hashlib
import random

import jwt
from flask import current_app


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
