# app/routes/province_routes.py
from flask import Blueprint
from controllers import region_controller

region_bp = Blueprint('region', __name__)

@region_bp.route('/provinces', methods=['GET'])
def get_provinces():
    return region_controller.get_provinces()

@region_bp.route('/regencies', methods=['GET'])
def get_regencies():
    return region_controller.get_regencies()

@region_bp.route('/districts', methods=['GET'])
def get_districts():
    return region_controller.get_districts()