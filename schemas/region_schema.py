from app import ma
from marshmallow import fields
from models import Province, Regency, District

class ProvinceSchema(ma.SQLAlchemyAutoSchema):
   class Meta:
       model = Province


class RegencySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
       model = Regency
       
    province = fields.Nested(ProvinceSchema)
    
    
class DistrictSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = District
    regency = fields.Nested(RegencySchema)