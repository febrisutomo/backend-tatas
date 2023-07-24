from flask import request, jsonify, Blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from marshmallow import ValidationError
from models import User
from schemas.user_schema import (
    RegisterSchema,
    UserSchema,
    LoginSchema,
    UpdateProfile,
)
from app import db, bcrypt
from utils.parse_nik import parse_nik
    
def check_email():
    data = request.get_json()
    print(str(data))

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email sudah digunakan"}), 409

    return jsonify({"message": "Email tersedia"})

def register():
    schema = RegisterSchema()
    data = request.get_json()
    
    try:
        validated = schema.load(data)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    if User.query.filter_by(email=validated["email"]).first():
        return jsonify({"message": "email sudah digunakan"}), 409

    try:
        new_user = User(**validated)
        pasword_hash = bcrypt.generate_password_hash(validated["password"]).decode('utf-8')
        new_user.password = pasword_hash
        if validated['nik']:
            nik_info = parse_nik(validated['nik'])
            new_user.birthday = nik_info['birthdate']
        
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Registrasi berhasil. Silahkan Login"})

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


def login():
    login_schema = LoginSchema()
    data = request.get_json()
    
    try:
        validated = login_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    user = User.query.filter_by(email=validated['email']).first()

    if not user or not bcrypt.check_password_hash(user.password, validated['password']):
        return jsonify({"message": "Email atau password tidak valid"}), 401

    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)

    return jsonify(
        {
            "message": "Login berhasil",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )


def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({"message": "Berhasil refresh token", "access_token": access_token})


def get_profile():
    schema = UserSchema()
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"success": False, "message": "User tidak ditemukan"}), 404
    
    return jsonify({"user": schema.dump(user)})
    
def update_profile():
    schema = UpdateProfile()
    email = get_jwt_identity()
    
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"success": False, "message": "User tidak ditemukan"}), 404
    
    data = request.get_json()
    try:
        validated = schema.load(data)
    except ValidationError as err:
        print(str(err.messages))
        return jsonify({"error": err.messages}), 400
    
    try:
        for key, value in validated.items():
            setattr(user, key, value)
        db.session.commit()
        return jsonify({"message": "Profil berhasil diperbarui"})
    
    except Exception as e:
        return jsonify({'message': 'An error occurred. ' + str(e)}), 500
    
    
def change_password():
    data = request.get_json()
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    
    
    if not bcrypt.check_password_hash(user.password, data['current_password']):
        return jsonify({"message": "Password saat ini tidak sesaui"}), 401
    
    try:
        user.password = bcrypt.generate_password_hash(
            data["new_password"]
        ).decode("utf-8")
        
        db.session.commit()
        
        return jsonify({'message': 'Password berhasil diubah'})
    
    except Exception as e:
        print(e)
        return jsonify({'message': 'Password gagal diubah diubah'}), 500
        