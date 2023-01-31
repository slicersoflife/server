from sqlalchemy import Column, SmallInteger, String, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """A model of a user."""
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True)

    name = Column(String(200))
    email = Column(String(200))
    password = Column(String(200))
    phone = Column(String(12))
    group_id = Column(UUID(as_uuid=True), primary_key=False)

    def __repr__(self):
        return f"User<{self.id} | {self.name}>"


class Group(Base):
    """A model of a group of users."""
    __tablename__ = 'groups'
    id = Column(UUID(as_uuid=True), primary_key=True)

    name = Column(String(200))

    def __repr__(self):
        return f"Group<{self.id} | {self.name}>"
