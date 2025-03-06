from ..database import db

class AssetGoalMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=False)
    allocation_percentage = db.Column(db.Float, nullable=False)
    
    asset = db.relationship('Asset', backref='goal_mappings')
    goal = db.relationship('Goal', backref='asset_mappings') 