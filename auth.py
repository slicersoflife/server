import datetime
from uuid import uuid4 as uuid
import jwt
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from models import User, Group

auth = Blueprint('auth', __name__)


def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=60),
            'iat': datetime.datetime.utcnow(),
            'sub': str(user_id)
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as exception:
        return exception


@auth.post('/register')
@cross_origin()
def register():
    session = Session()

    # get the post data
    post_data = request.get_json()
    # check if user already exists
    user = session.query(User).filter_by(email=post_data.get('email')).first()
    if user:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return jsonify(response_object), 202

    try:
        group = session.query(Group).filter_by(id=post_data.get('group_id')).first()
        if not group:
            response_object = {
                'status': 'fail',
                'message': f'Group with id {post_data.get("group_id")} does not exist.'
            }
            return jsonify(response_object), 401

        user = User(
            id=uuid(),
            email=post_data.get('email'),
            password=post_data.get('password'),
            phone=post_data.get('phone'),
            group_id=post_data.get('group_id')
        )
        session.add(user)
        session.commit()

        # generate the auth token
        auth_token = encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'auth_token': auth_token
        }
        return jsonify(response_object), 201

    except Exception as exception:
        print(exception)
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return jsonify(response_object), 401


@auth.post('/login')
@cross_origin()
def login():
    session = Session()

    # get the post data
    post_data = request.get_json()
    try:
        # fetch the user data
        user = session.query(User).filter_by(email=post_data.get('email')).first()
        if not user:
            response_object = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return jsonify(response_object), 404

        if user.password != post_data.get('password'):
            response_object = {
                'status': 'fail',
                'message': 'Wrong password.'
            }
            return jsonify(response_object), 401

        auth_token = encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully logged in.',
            'auth_token': auth_token
        }
        return jsonify(response_object), 200

    except Exception as exception:
        print(exception)
        response_object = {
            'status': 'fail',
            'message': str(exception)
        }
        return jsonify(response_object), 500
