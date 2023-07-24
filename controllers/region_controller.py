from flask import jsonify, request
from models import Province, Regency, District
from schemas.region_schema import ProvinceSchema, RegencySchema, DistrictSchema
  
def get_provinces():
  provinces = Province.query.all()
  return jsonify({"provinces": ProvinceSchema(many=True).dump(provinces)})

def get_regencies():
  province_id = request.args.get("province_id")
  regencies = Regency.query.filter_by(province_id=province_id).all()
  if not regencies:
      return jsonify({"message": 'Kabupaten tidak ditemukan'}), 404
    
  return jsonify({"regencies": RegencySchema(many=True).dump(regencies)})

def get_districts():
  regency_id = request.args.get("regency_id")
  districts = District.query.filter_by(regency_id=regency_id).all()
  if not districts:
      return jsonify({"message": 'Kecamatan tidak ditemukan'}), 404
    
  return jsonify({"districts": DistrictSchema(many=True).dump(districts)})