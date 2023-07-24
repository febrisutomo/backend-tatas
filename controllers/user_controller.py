from flask import jsonify
from models import User
from schemas.user_schema import UserSchema

def get_users():
  users = User.query.all()
  return jsonify({"users": UserSchema(many=True).dump(users)})

def get_user(id):
  user = User.query.get(id)
  if not user:
      return jsonify({"message": 'User tidak ditemukan'}), 404
    
  return jsonify({"user": UserSchema().dump(user)})