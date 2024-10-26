from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app import db


class SuspiciousAddress(db.Model):
    __tablename__ = 'suspicious_addresses'

    id = Column(Integer, primary_key=True)
    address = Column(String(80), unique=True, nullable=False)
    cryptocurrency = Column(String(10), nullable=False)
    reason = Column(String(255), nullable=True)  # 필드 포함
    risk_score = Column(Integer, nullable=True)
    first_seen = Column(DateTime, nullable=False)
    last_seen = Column(DateTime, nullable=False)

    def __init__(self, address, cryptocurrency, reason, first_seen, last_seen,
                 risk_score):
        self.address = address
        self.cryptocurrency = cryptocurrency
        self.reason = reason
        self.first_seen = first_seen
        self.last_seen = last_seen
        self.risk_score = risk_score

    def __repr__(self):
        return f'<SuspiciousAddress {self.address}>'


class AddressCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    check_date = db.Column(db.DateTime, default=datetime.utcnow)
    result = db.Column(db.Boolean, default=False)

    def __init__(self, address, result):
        self.address = address
        self.result = result

    def __repr__(self):
        return f'<AddressCheck {self.address}>'
