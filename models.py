from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """A model of a user."""
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True)

    display_name = Column(String(200))
    username = Column(String(200))
    phone = Column(String(12))

    def __repr__(self):
        return f"User<{self.id} | {self.name}>"
