import datetime
import os
from uuid import uuid4 as uuid

import jwt
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_httpauth import HTTPTokenAuth
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from twilio.rest import Client

from models import User, Group, Base

Session = sessionmaker()
app = Flask(__name__)
cors = CORS(app)
app.config.from_object('config.BaseConfig')
auth = HTTPTokenAuth(scheme='Bearer')


def init_endpoints(engine: Engine):
    Session.configure(bind=engine)

    @auth.verify_token
    def verify_token(token):
        data = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms='HS256')
        session = Session()

        user = session.query(User).filter_by(id=data["sub"]).first()
        return user

    @app.get('/group')
    @cross_origin()
    def get_group():
        session = Session()
        groups = session.query(Group).all()
        response_object = {
            'status': 'success',
            'groups': [
                {'name': group.name, 'id': group.id} for group in groups
            ]
        }
        return jsonify(response_object), 200

    @app.post('/group')
    @cross_origin()
    @auth.login_required
    def post_group():
        session = Session()

        # get the post data
        post_data = request.get_json()
        try:
            new_group = Group(
                id=uuid(),
                name=post_data.get('name')
            )
            session.add(new_group)
            session.commit()

            response_object = {
                'status': 'success',
                'message': 'Successfully added new group.',
                'group_id': str(new_group.id)
            }
            return jsonify(response_object), 201

        except Exception as exception:
            response_object = {
                'status': 'fail',
                'message': str(exception)
            }
            return jsonify(response_object), 500
        
    @app.post('/sms')
    @auth.login_required
    def sms():
        session = Session()
        post_data = request.get_json()
        my_phone = session.query(User).filter_by(id=post_data.get('user_id')).first().phone
        all_phones = [u.phone for u in session.query(User).all()]
        phone_number = None
        for phone in all_phones:
            if phone != my_phone:
                phone_number = phone
        account_sid = 'AC8db8d6f7af13addc2bee16c95f9e3a9a' 
        auth_token = 'ebf123106d43cba081e81f8f2fdf577d' 
        client = Client(account_sid, auth_token)
        post_data = request.get_json()

        message = client.messages.create(  
                            messaging_service_sid='MGe9ac5c560345a70da6df56a735f0bea0', 
                            body='Heres your daily reminder to connect with your friends! \
                            Join the Slice of Life chat through this link: ' + post_data.get('link'),
                            to=phone_number
                        )
        return jsonify({"message": "success"})
        

if __name__ == '__main__':
    app.run()


def load_app():
    load_dotenv()
    engine = create_engine(os.getenv("DATABASE_URL"), connect_args={'sslmode': 'verify-ca'})
    Base.metadata.create_all(engine)
    init_endpoints(engine)
    print("Connected to database.")

    return app


if __name__ == "__main__":
    app = load_app()
    app.run()

