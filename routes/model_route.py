from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required
from app import app
from engine import nb_engine
import os

model_bp = Blueprint("model", __name__)

@model_bp.route("/evaluate", methods=["GET"])
@jwt_required()
def evaluate_model():
    result = nb_engine.evaluate_model()
    return jsonify({"result": result})


@model_bp.route("/", methods=["GET"])
@jwt_required()
def list_files():
    file_list = []
    for filename in os.listdir(app.config["UPLOAD_FOLDER"]):
        file_list.append(filename)
    return jsonify({"files": file_list}), 200


@model_bp.route("/", methods=["POST"])
@jwt_required()
def upload_file():
    print(request.files["file"])
    if "file" not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    if file:
        # filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], "thalassemia_3v_raw.xlsx"))
        return jsonify({"message": "File successfully uploaded"}), 200
    else:
        return jsonify({"message": "File upload failed"}), 500


@model_bp.route("/<filename>", methods=["DELETE"])
@jwt_required()
def delete_file(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if not os.path.exists(file_path):
        return jsonify({"message": "File not found"}), 404

    try:
        os.remove(file_path)
        return jsonify({"message": "File deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Failed to delete file: {str(e)}"}), 500


@model_bp.route("/download-dataset", methods=["GET"])
@jwt_required()
def download_dataset():
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], "thalassemia_3v_raw.xlsx")

    if not os.path.exists(file_path):
        return jsonify({"message": "File not found"}), 404

    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"message": f"Failed to download file: {str(e)}"}), 500
