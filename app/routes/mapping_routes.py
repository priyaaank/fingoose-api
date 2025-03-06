from flask import Blueprint, request, jsonify
from ..models.asset_goal_mapping import AssetGoalMapping
from ..models.asset import Asset
from ..models.goal import Goal
from ..database import db

bp = Blueprint('mappings', __name__, url_prefix='/api/mappings', static_folder=None)

@bp.route('/', methods=['POST'])
def create_mapping():
    data = request.get_json()
    
    mapping = AssetGoalMapping(
        asset_id=data['asset_id'],
        goal_id=data['goal_id'],
        allocation_percentage=data['allocation_percentage']
    )
    
    db.session.add(mapping)
    db.session.commit()
    
    return jsonify({
        'id': mapping.id,
        'message': 'Mapping created successfully'
    }), 201

@bp.route('/', methods=['GET'])
def get_mappings():
    mappings = AssetGoalMapping.query.all()
    return jsonify([{
        'id': mapping.id,
        'asset_id': mapping.asset_id,
        'goal_id': mapping.goal_id,
        'allocation_percentage': mapping.allocation_percentage,
        'asset_name': mapping.asset.name,
        'goal_name': mapping.goal.name
    } for mapping in mappings]) 