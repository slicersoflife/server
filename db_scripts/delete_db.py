import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"), connect_args={"sslmode": "verify-ca"})
connection = engine.connect()
print(connection.execute(text("DELETE FROM groups")))
