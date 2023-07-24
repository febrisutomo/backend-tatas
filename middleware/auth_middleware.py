from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models.user import User
from schemas.user_schema import UserSchema

def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            user = UserSchema().dump(User.query.filter_by(email=current_user).first())

            if user['role']['name'] not in roles:
                return jsonify({'message': 'Unauthorized'}), 403

            return fn(*args, **kwargs)

        return wrapper

    return decorator
