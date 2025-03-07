from datetime import datetime
from ..database import db
from .utils import RoundingMixin

class Asset(db.Model, RoundingMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(10, collation='utf8mb4_unicode_ci'), nullable=False)  # For emoji
    asset_type = db.Column(db.String(50), nullable=False)  # e.g., "Mutual Fund", "Fixed Deposit", etc.
    current_value = db.Column(db.Float, nullable=False)
    projected_roi = db.Column(db.Float, nullable=False)
    maturity_year = db.Column(db.Integer, nullable=False)
    additional_comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Relationship to goals through mappings
    goals = db.relationship('Goal', 
                          secondary='asset_goal_mapping',
                          backref=db.backref('assets', lazy='dynamic'),
                          lazy='dynamic')
    mappings = db.relationship('AssetGoalMapping',
                             cascade='all, delete-orphan',
                             backref='asset') 

    def to_dict(self):
        """Convert asset to dictionary with rounded values"""
        # Get goal mappings
        goal_mappings = [{
            'goal_id': mapping.goal_id,
            'goal_name': mapping.goal.name,
            'allocation_percentage': mapping.allocation_percentage
        } for mapping in self.mappings]
        
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'asset_type': self.asset_type,
            'current_value': self.round_amount(self.current_value),
            'projected_roi': self.projected_roi,
            'maturity_year': self.maturity_year,
            'additional_comments': self.additional_comments,
            'goal_mappings': goal_mappings,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 