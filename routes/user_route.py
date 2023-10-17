# app/routes/user_routes.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from middleware.auth_middleware import role_required
from models import User
from schemas.user_schema import UserSchema

user_bp = Blueprint("user", __name__)


@user_bp.route("/", methods=["GET"])
@jwt_required()
@role_required("Admin")
def get_users():
    users = User.query.all()
    return jsonify({"users": UserSchema(many=True).dump(users)})


@user_bp.route("/<id>", methods=["GET"])
@jwt_required()
@role_required("Admin")
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User tidak ditemukan"}), 404

    return jsonify({"user": UserSchema().dump(user)})
