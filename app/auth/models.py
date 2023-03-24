from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import INT

from app.extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True)
    display_name = Column(String(50), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    phone = Column(String(20), nullable=False, unique=True)
    profile_picture_url = Column(String(255), nullable=True)
    friend_requests_sent = relationship('FriendRequest', foreign_keys='FriendRequest.from_user_id')
    friend_requests_received = relationship('FriendRequest', foreign_keys='FriendRequest.to_user_id')

    def __repr__(self):
    return f"User<{self.id} | {self.username}>"

class FriendRequest(db.model):
    __tablename__ = 'friend_requests'

    id_requests = Column(UUID, primary_key=True)
    from_user_id = Column(String, ForeignKey('users.id'), nullable=False)
    to_user_id = Column(String, ForeignKey('users.id'), nullable=False)
    status = Column(Enum('accepted', 'rejected', 'pending'), nullable=False)

