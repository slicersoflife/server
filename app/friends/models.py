from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db


class FriendRequest(db.Model):
    __tablename__ = "friend_requests"

    id = Column(UUID, primary_key=True)
    from_user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    accepted = Column(Boolean, nullable=False)
