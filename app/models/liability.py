from datetime import datetime
from ..database import db
from .utils import RoundingMixin

class Liability(db.Model, RoundingMixin):
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

    def to_dict(self):
        """Convert liability to dictionary with rounded values"""
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'icon': self.icon,
            'borrowed_principle': self.round_amount(self.borrowed_principle),
            'current_outstanding': self.round_amount(self.current_outstanding),
            'rate_of_interest': self.rate_of_interest,
            'emi': self.round_amount(self.emi),
            'remaining_tenure': self.remaining_tenure,
            'total_tenure': self.total_tenure,
            'start_date': self.start_date.strftime('%Y-%m'),
            'additional_comments': self.additional_comments,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 