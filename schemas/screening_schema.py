from app import ma
from models import Screening
from marshmallow import fields
from .user_schema import UserSchema

class ScreeningSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Screening
        include_fk = True

class ScreeningAdminSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Screening
        include_fk = True
    user = fields.Nested(UserSchema)
       