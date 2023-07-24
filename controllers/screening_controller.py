from flask import jsonify, request
from models import User, Screening
from flask_jwt_extended import get_jwt_identity
from schemas.screening_schema import ScreeningSchema
from marshmallow import ValidationError
from app import db
from engine import nb_engine


def get_histories(user_id):
  schema = ScreeningSchema(many=True)
  page = int(request.args.get("page", 1))
  per_page = int(request.args.get("per_page", 5))
  items = (
      Screening.query.filter_by(user_id=user_id)
      .order_by(Screening.date.desc())
      .paginate(page=page, per_page=per_page, error_out=False)
  )
  result = {
      "total_pages": items.pages,
      "current_page": items.page,
      "items_per_page": per_page,
      "total_items": items.total,
      "screenings": schema.dump(items),
  }
  if items.has_next:
      result["next_page"] = items.next_num
  return jsonify(result)


def get_result(user_id):
  schema = ScreeningSchema()
  screening = (
      Screening.query.filter_by(user_id=user_id)
      .order_by(Screening.date.desc())
      .first()
  )
  
  if screening is None:
    return jsonify({"message": "User belum melakukan screening"}), 404
 
  return jsonify({"screening": schema.dump(screening)})

  
def get_my_histories():
  email = get_jwt_identity()
  user = User.query.filter_by(email=email).first()
  return get_histories(user.id)


def get_my_result():
  email = get_jwt_identity()
  user = User.query.filter_by(email=email).first()
  return get_result(user.id)

  
def add(user_id):
  schema = ScreeningSchema()
  try:  
    data = request.get_json()
    data['user_id'] = user_id

    try:
        validated = schema.load(data)
    except ValidationError as err:
      return jsonify({"error": err.messages}), 400
      
    val = [data["hb"], data["mcv"], data["mch"]]
    result = nb_engine.cekkemungkinan(val)
    probability = round(result["probabilitas"], 2)
    prediction = True if result["prediksi"] == "Positif" else False
    

    screening = Screening(**validated, probability = probability, prediction=prediction)
    
    db.session.add(screening)
    db.session.commit()
    
    return jsonify({"message": "Screening berhasil", "result": result})

  except Exception as e:
    print(e)
    return jsonify({"error": str(e)}), 500
    
    
def add_for_myself():
  email = get_jwt_identity()
  user = User.query.filter_by(email=email).first()
  return add(user.id)
