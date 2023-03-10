from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import Base


class User(Base):
    """A model of a user."""

    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True)

    display_name = Column(String(200))
    username = Column(String(200))
    phone = Column(String(200))
    profile_picture_url = Column(String(200))

    def __repr__(self):
        return f"User<{self.id} | {self.username}>"
