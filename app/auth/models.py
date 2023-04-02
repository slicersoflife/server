from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.extensions import db
from app.friends.models import Friend, FriendRequest


class User(db.Model):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    display_name = Column(String(50), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    phone = Column(String(20), nullable=False, unique=True)
    profile_picture_url = Column(String(255), nullable=True)

    friends_a = relationship(
        "User",
        secondary=Friend.__tablename__,
        primaryjoin=id == Friend.user_a_id,
        secondaryjoin=id == Friend.user_b_id,
        viewonly=True,
    )
    friends_b = relationship(
        "User",
        secondary=Friend.__tablename__,
        primaryjoin=id == Friend.user_b_id,
        secondaryjoin=id == Friend.user_a_id,
        viewonly=True,
    )
    friend_requests_sent = relationship(
        "User",
        secondary=FriendRequest.__tablename__,
        primaryjoin=id == FriendRequest.from_user_id,
        secondaryjoin=id == FriendRequest.to_user_id,
        viewonly=True,
    )
    friend_requests_received = relationship(
        "User",
        secondary=FriendRequest.__tablename__,
        primaryjoin=id == FriendRequest.to_user_id,
        secondaryjoin=id == FriendRequest.from_user_id,
        viewonly=True,
    )

    def __repr__(self):
        return f"User<{self.id} | {self.username}>"
