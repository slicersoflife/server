from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from .models import User


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User

    id = auto_field()
    display_name = auto_field()
    username = auto_field()


user_schema = UserSchema()
