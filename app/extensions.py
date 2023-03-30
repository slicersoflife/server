import os

from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from twilio.rest import Client

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()
twilio = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
cache = Redis(decode_responses=True)
