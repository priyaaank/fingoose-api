from datetime import datetime
from ..database import db

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(200))
    current_value = db.Column(db.Float, nullable=False)
    projected_roi = db.Column(db.Float, nullable=False)
    maturity_month = db.Column(db.Integer)  # 1-12, nullable
    maturity_year = db.Column(db.Integer)   # nullable
    additional_comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 