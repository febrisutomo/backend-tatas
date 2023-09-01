from flask import Blueprint
from flask_jwt_extended import jwt_required

from middleware.auth_middleware import role_required

from controllers import auth_controller

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/check-username", methods=["POST"])
def check_username():
    return auth_controller.check_username()


@auth_bp.route("/register", methods=["POST"])
def register():
    return auth_controller.register()


@auth_bp.route("/login", methods=["POST"])
def login():
   return auth_controller.login()

@auth_bp.route("/change-password", methods=["PATCH"])
@jwt_required()
def change_password():
   return auth_controller.change_password()


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    return auth_controller.get_profile()

@auth_bp.route("/profile", methods=["PATCH"])
@jwt_required()
def update_profile():
    return auth_controller.update_profile()

@auth_bp.route("/refresh-token", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    return auth_controller.refresh_token()
