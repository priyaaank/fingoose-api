from datetime import datetime
from ..database import db
import math

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

    @property
    def projected_value(self):
        """
        Calculate projected value using compound interest formula
        Using July (month 7) for both years to get exact mid-year calculation
        """
        years = self.target_year - self.goal_creation_year
        # Convert percentage to decimal
        rate = self.projected_inflation / 100
        return self.initial_goal_value * math.pow(1 + rate, years)

    def to_dict(self):
        """Convert goal to dictionary with computed projected value"""
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'goal_creation_year': self.goal_creation_year,
            'target_year': self.target_year,
            'projected_inflation': self.projected_inflation,
            'initial_goal_value': self.initial_goal_value,
            'projected_value': self.projected_value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 