from ..database import db

class AssetGoalMapping(db.Model):
    __tablename__ = 'asset_goal_mapping'
    
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id', ondelete='CASCADE'), primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id', ondelete='CASCADE'), primary_key=True)
    allocation_percentage = db.Column(db.Float, nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('asset_id', 'goal_id', name='uq_asset_goal'),
    ) 