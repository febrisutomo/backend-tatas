from flask import Blueprint
from controllers import screening_controller
from flask_jwt_extended import jwt_required
from middleware.auth_middleware import role_required
screening_bp = Blueprint('screening', __name__)

@screening_bp.route('/me', methods=['POST'])
@jwt_required()
def add_for_myself():
    return screening_controller.add_for_myself()

@screening_bp.route("/me", methods=["GET"])
@jwt_required()
def get_my_result():
    return screening_controller.get_my_result()

@screening_bp.route("/me/history", methods=["GET"])
@jwt_required()
def get_my_histories():
    return screening_controller.get_my_histories()