from datetime import datetime
from ..database import db
from .utils import RoundingMixin

class Asset(db.Model, RoundingMixin):
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
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'icon': self.icon,
            'current_value': self.round_amount(self.current_value),
            'projected_roi': self.projected_roi,
            'maturity_date': f"{self.maturity_year}-{self.maturity_month:02d}" if self.maturity_month and self.maturity_year else None,
            'additional_comments': self.additional_comments,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 