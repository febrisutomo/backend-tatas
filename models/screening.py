from app import db
from datetime import datetime

class Screening(db.Model):
    __tablename__ = 'screenings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    hb = db.Column(db.Float(), nullable=False) 
    mch = db.Column(db.Float(), nullable=False) 
    mcv = db.Column(db.Float(), nullable=False) 
    probability = db.Column(db.Float()) 
    prediction = db.Column(db.Boolean)
    dna = db.Column(db.Boolean)
    verified = db.Column(db.Boolean, default=0)

    user = db.relationship('User', backref='screenings')
    
    def __init__(self, user_id, hb, mch, mcv, probability, prediction):
        self.user_id = user_id
        self.hb = hb
        self.mch = mch
        self.mcv = mcv
        self.probability = probability
        self.prediction = prediction