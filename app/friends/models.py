from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db


class Friend(db.Model):
    __tablename__ = "friends"

    id = Column(UUID, primary_key=True)
    user_a_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    user_b_id = Column(UUID, ForeignKey("users.id"), nullable=False)


class FriendRequest(db.Model):
    __tablename__ = "friend_requests"

    id = Column(UUID, primary_key=True)
    from_user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
