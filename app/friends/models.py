from sqlalchemy import Column, String, relationship, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db


class FriendRequest(db.model):
    __tablename__ = "friend_requests"

    id = Column(UUID, primary_key=True)
    from_user_id = Column(String, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(String, ForeignKey("users.id"), nullable=False)
    status = Column(Enum("accepted", "pending"), nullable=False)
