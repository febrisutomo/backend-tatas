# app/models/user.py
from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False, default=2)
    gender_id = db.Column(db.Integer, db.ForeignKey('genders.id'))
    nik = db.Column(db.String(16))
    birthday = db.Column(db.Date)
    blood_type_id = db.Column(db.Integer, db.ForeignKey('blood_types.id'))
    district_id = db.Column(db.Integer, db.ForeignKey('districts.id'))
    address = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    current_latitude = db.Column(db.Float)
    current_longitude =db. Column(db.Float)
    phone_number = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    district = db.relationship('District', backref='users')
    role = db.relationship('Role', backref='users')
    gender = db.relationship('Gender', backref='users')
    blood_type = db.relationship('BloodType', backref='users')

    def __init__(
        self,
        email,
        password=None,
        role_id=2,
        nik=None,
        name=None,
        birthday=None,
        gender_id=None,
        blood_type_id=None,
        district_id=None,
        address=None,
        latitude=None,
        longitude=None,
        phone_number=None,
    ):
        self.email = email
        self.password = password
        self.role_id = role_id
        self.nik = nik
        self.name = name
        self.birthday = birthday
        self.gender_id = gender_id
        self.blood_type_id = blood_type_id
        self.district_id = district_id
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.phone_number = phone_number,
    
class Role(db.Model):
    __tablename__ = "roles"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


class Gender(db.Model):
    __tablename__ = 'genders'  # Nama tabel dengan bentuk plural

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


class BloodType(db.Model):
    __tablename__ = 'blood_types'  # Nama tabel dengan bentuk plural

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name