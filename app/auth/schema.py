from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from .models import User


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User

    id = auto_field()
    display_name = auto_field()
    username = auto_field()
    friends = fields.Method("serialize_friends")
    friend_requests_sent = fields.Nested(
        "UserSchema",
        many=True,
        only=("id", "display_name", "username"),
    )
    friend_requests_received = fields.Nested(
        "UserSchema",
        many=True,
        only=("id", "display_name", "username"),
    )

    @staticmethod
    def serialize_friends(obj):
        friends = []
        for friend in obj.friends_a:
            friends.append(friend)
        for friend in obj.friends_b:
            friends.append(friend)
        return users_schema.dump(friends)


user_schema = UserSchema()
users_schema = UserSchema(many=True, only=("id", "username", "display_name"))
