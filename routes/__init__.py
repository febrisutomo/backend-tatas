from flask import Blueprint
from .auth_routes import auth_bp
from .user_route import user_bp
from .region_route import region_bp
from .screening_route import screening_bp

api_v1 = Blueprint("api_v1", __name__)

api_v1.register_blueprint(auth_bp, url_prefix="/auth")
api_v1.register_blueprint(user_bp, url_prefix="/users")
api_v1.register_blueprint(screening_bp, url_prefix="/screenings")
api_v1.register_blueprint(region_bp)