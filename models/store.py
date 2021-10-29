from models.init import db
from dataclasses import dataclass

@dataclass
class Address(db.Model):
    __tablename__ = 'address'
    id: int
    address: str
    balance: int
    rewards: int
    referral_code: str
    referral_count: int

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(10000))
    balance = db.Column(db.Integer)
    rewards = db.Column(db.Integer)
    referral_count = db.Column(db.Integer)
    referral_code = db.Column(db.Text)
    
@dataclass
class Referral(db.Model):
    __tablename__ = 'referral'
    id: int
    address: str
    
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(10000))
    referral = db.relationship(Address, backref='referral', lazy=True)
    referral_id = db.Column(db.Integer(), db.ForeignKey(Address.id))
    

    
