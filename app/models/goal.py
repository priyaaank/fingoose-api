from datetime import datetime
from ..database import db

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(10, collation='utf8mb4_unicode_ci'), nullable=False)  # For emoji
    goal_creation_year = db.Column(db.Integer, nullable=False)
    target_year = db.Column(db.Integer, nullable=False)
    projected_inflation = db.Column(db.Float, nullable=False)
    initial_goal_value = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Relationship to mappings
    mappings = db.relationship('AssetGoalMapping',
                             cascade='all, delete-orphan',
                             backref='goal') 