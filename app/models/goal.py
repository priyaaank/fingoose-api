from datetime import datetime
from ..database import db

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_value = db.Column(db.Float, nullable=False)
    target_month = db.Column(db.Integer, nullable=False)  # 1-12
    target_year = db.Column(db.Integer, nullable=False)
    expected_inflation = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Relationship to mappings
    mappings = db.relationship('AssetGoalMapping',
                             cascade='all, delete-orphan',
                             backref='goal') 