from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db
from app.friends.models import FriendRequest


class User(db.Model):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    display_name = Column(String(50), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    phone = Column(String(20), nullable=False, unique=True)
    profile_picture_url = Column(String(255), nullable=True)
    friend_requests_sent = db.relationship(
        "User",
        secondary=FriendRequest.__tablename__,
        foreign_keys=FriendRequest.from_user_id,
    )
    friend_requests_received = db.relationship(
        "User",
        secondary=FriendRequest.__tablename__,
        foreign_keys=FriendRequest.to_user_id,
    )

    def __repr__(self):
        return f"User<{self.id} | {self.username}>"
