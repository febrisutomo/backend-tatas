from app import ma
from models import Screening

class ScreeningSchema(ma.SQLAlchemyAutoSchema):
   class Meta:
       model = Screening
       include_fk = True
       
       