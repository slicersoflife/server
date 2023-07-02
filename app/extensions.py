import os

from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from twilio.rest import Client

import boto3, botocore

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()
twilio = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
cache = Redis(host=os.getenv("REDIS_HOST"), port=6379, decode_responses=True)
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
    region_name="us-east-1",
)
