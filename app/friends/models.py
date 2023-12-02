from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db


class Friendship(db.Model):
    __tablename__ = "friendships"

    user_a_id = Column(UUID, ForeignKey("users.id"), nullable=False, primary_key=True)
    user_b_id = Column(UUID, ForeignKey("users.id"), nullable=False, primary_key=True)


class FriendRequest(db.Model):
    __tablename__ = "friend_requests"

    from_user_id = Column(
        UUID, ForeignKey("users.id"), nullable=False, primary_key=True
    )
    to_user_id = Column(UUID, ForeignKey("users.id"), nullable=False, primary_key=True)
