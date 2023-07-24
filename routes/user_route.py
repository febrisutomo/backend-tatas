# app/routes/user_routes.py
from flask import Blueprint
from controllers import user_controller
from flask_jwt_extended import jwt_required
from middleware.auth_middleware import role_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
@jwt_required()
@role_required('Admin')
def get_users():
    return user_controller.get_users()

@user_bp.route("/<id>", methods=["GET"])
@jwt_required()
@role_required('Admin')
def get_user(id):
    return user_controller.get_user(id)