from flask import jsonify, request, send_file
from models import User, Screening
from flask_jwt_extended import get_jwt_identity
from schemas.screening_schema import ScreeningSchema, ScreeningAdminSchema
from marshmallow import ValidationError
from app import db, app
from engine import nb_engine
from werkzeug.utils import secure_filename
import os

def get_all():
  schema = ScreeningAdminSchema(many=True)
  page = int(request.args.get("page", 1))
  per_page = int(request.args.get("per_page", 5))
  items = (
      Screening.query
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


def update_dna(screening_id):
  try:
    data = request.get_json()
    screening = Screening.query.get(screening_id)
  
    if(data['dna'] == 'null'):
      screening.dna = None
    else:
      screening.dna = int(data['dna'])
  
    db.session.commit()
    return jsonify({'message': 'Hasil DNA berhasil diubah'})
    
  except Exception as e:
    print(e)
    return jsonify({'message': 'Hasil DNA gagal diubah'}), 500


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
  username = get_jwt_identity()
  user = User.query.filter_by(username=username).first()
  return get_histories(user.id)


def get_my_result():
  username = get_jwt_identity()
  user = User.query.filter_by(username=username).first()
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
    result = nb_engine.check_probability(val)
    print(result)
    probability = round(result["probability"], 2)
    prediction = result["prediction"]
    

    screening = Screening(**validated, probability = probability, prediction=prediction)
    
    db.session.add(screening)
    db.session.commit()
    
    return jsonify({"message": "Screening berhasil", "result": result})

  except Exception as e:
    print(e)
    return jsonify({"error": str(e)}), 500
    
    
def add_for_myself():
  username = get_jwt_identity()
  user = User.query.filter_by(username=username).first()
  return add(user.id)

def evaluate_model():
  result = nb_engine.evaluate_model()
  return jsonify({"result": result})

def upload_file():
    print(request.files['file'])
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        # filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'thalassemia_3v_raw.xlsx'))
        return jsonify({'message': 'File successfully uploaded'}), 200
    else:
        return jsonify({'message': 'File upload failed'}), 500
      
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(file_path):
        return jsonify({'message': 'File not found'}), 404

    try:
        os.remove(file_path)
        return jsonify({'message': 'File deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Failed to delete file: {str(e)}'}), 500
      
# def list_files():
#     file_list = []
#     for filename in os.listdir(app.config['UPLOAD_FOLDER']):
#         file_list.append(filename)
#     return jsonify({"files": file_list}), 200
  
def download_dataset():
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thalassemia_3v_raw.xlsx')

    if not os.path.exists(file_path):
        return jsonify({'message': 'File not found'}), 404

    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'message': f'Failed to download file: {str(e)}'}), 500