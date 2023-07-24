from marshmallow import Schema, fields, validate
from app import ma
from models import User, Gender, BloodType, Role
from .region_schema import DistrictSchema


class RoleSchema(ma.SQLAlchemyAutoSchema):
   class Meta:
       model = Role


class GenderSchema(ma.SQLAlchemyAutoSchema):
   class Meta:
       model = Gender


class BloodTypeSchema(ma.SQLAlchemyAutoSchema):
   class Meta:
       model = BloodType



class RegisterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
    
    nik = fields.Str(validate=validate.Length(equal=16))
    
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ['password']
    
    blood_type = fields.Nested(BloodTypeSchema)
    gender = fields.Nested(GenderSchema)
    role = fields.Nested(RoleSchema)
    district = fields.Nested(DistrictSchema)
    
class UpdateProfile(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ['password', 'email']
        include_fk = True
        
    

