from flask import Blueprint
from controllers import screening_controller
from flask_jwt_extended import jwt_required
from middleware.auth_middleware import role_required
screening_bp = Blueprint('screening', __name__)

@screening_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all():
    return screening_controller.get_all()

@screening_bp.route('/<screening_id>', methods=['PATCH'])
@jwt_required()
def update_dna(screening_id):
    return screening_controller.update_dna(screening_id)

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

@screening_bp.route("/evaluate-model", methods=["GET"])
@jwt_required()
def evaluate_model():
    return screening_controller.evaluate_model()

@screening_bp.route("/list-files", methods=["GET"])
@jwt_required()
def list_files():
    return screening_controller.list_files()

@screening_bp.route("/upload-dataset", methods=["POST"])
@jwt_required()
def upload_file():
    return screening_controller.upload_file()

@screening_bp.route("/delete-file/<filename>", methods=["DELETE"])
@jwt_required()
def delete_file(filename):
    return screening_controller.delete_file(filename)

@screening_bp.route("/download-dataset", methods=["GET"])
@jwt_required()
def download_dataset():
    return screening_controller.download_dataset()
