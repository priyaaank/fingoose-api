from datetime import datetime
from ..database import db

class Liability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(200))
    borrowed_principle = db.Column(db.Float, nullable=False)
    current_outstanding = db.Column(db.Float, nullable=False)
    rate_of_interest = db.Column(db.Float, nullable=False)
    emi = db.Column(db.Float, nullable=False)
    remaining_tenure = db.Column(db.Integer, nullable=False)
    total_tenure = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    additional_comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 