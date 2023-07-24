from app import db

class Province(db.Model):
    __tablename__ = 'provinces'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Regency(db.Model):
    __tablename__ = 'regencies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    province_id = db.Column(db.Integer, db.ForeignKey('provinces.id'), nullable=False)
    province = db.relationship('Province', backref='regencies')


class District(db.Model):
    __tablename__ = 'districts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    regency_id = db.Column(db.Integer, db.ForeignKey('regencies.id'), nullable=False)
    regency = db.relationship('Regency', backref='districts')