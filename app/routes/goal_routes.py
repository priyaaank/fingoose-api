from flask import Blueprint, request, jsonify
from ..models.goal import Goal
from ..models.asset import Asset
from ..models.asset_goal_mapping import AssetGoalMapping
from ..database import db

bp = Blueprint('goals', __name__, url_prefix='/api/goals', static_folder=None)

def validate_asset_mappings(asset_mappings):
    """Validate asset mappings data"""
    if not isinstance(asset_mappings, list):
        raise ValueError("asset_mappings must be a list")
    
    total_allocation = 0
    asset_ids = set()
    
    for mapping in asset_mappings:
        if not isinstance(mapping, dict):
            raise ValueError("Each mapping must be an object")
        
        if 'asset_id' not in mapping or 'allocation_percentage' not in mapping:
            raise ValueError("Each mapping must have asset_id and allocation_percentage")
        
        allocation = float(mapping['allocation_percentage'])
        if allocation <= 0 or allocation > 100:
            raise ValueError("Allocation percentage must be between 0 and 100")
        
        if mapping['asset_id'] in asset_ids:
            raise ValueError(f"Duplicate asset_id found: {mapping['asset_id']}")
        
        asset_ids.add(mapping['asset_id'])
        total_allocation += allocation
    
    if total_allocation > 100:
        raise ValueError("Total allocation percentage cannot exceed 100%")
    
    return True

@bp.route('', methods=['POST'])
def create_goal():
    data = request.get_json()
    
    try:
        goal = Goal(
            name=data['name'],
            icon=data['icon'],
            goal_creation_year=data['goal_creation_year'],
            target_year=data['target_year'],
            projected_inflation=data['projected_inflation'],
            initial_goal_value=data['initial_goal_value']
        )
        
        db.session.add(goal)
        
        # Handle asset mappings if provided
        if 'asset_mappings' in data:
            try:
                validate_asset_mappings(data['asset_mappings'])
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
            
            for mapping in data['asset_mappings']:
                asset = Asset.query.get(mapping['asset_id'])
                if not asset:
                    return jsonify({'error': f"Asset not found with id: {mapping['asset_id']}"}), 404
                
                asset_goal_mapping = AssetGoalMapping(
                    goal=goal,
                    asset=asset,
                    allocation_percentage=mapping['allocation_percentage']
                )
                db.session.add(asset_goal_mapping)
        
        db.session.commit()
        
        return jsonify({
            'id': goal.id,
            'message': 'Goal created successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('', methods=['GET'])
def get_goals():
    goals = Goal.query.all()
    return jsonify([goal.to_dict() for goal in goals])

@bp.route('/<int:id>', methods=['GET'])
def get_goal(id):
    goal = Goal.query.get_or_404(id)
    return jsonify(goal.to_dict())

@bp.route('/<int:id>', methods=['PUT'])
def update_goal(id):
    goal = Goal.query.get_or_404(id)
    data = request.get_json()
    
    try:
        if 'name' in data:
            goal.name = data['name']
        if 'icon' in data:
            goal.icon = data['icon']
        if 'goal_creation_year' in data:
            goal.goal_creation_year = data['goal_creation_year']
        if 'target_year' in data:
            goal.target_year = data['target_year']
        if 'projected_inflation' in data:
            goal.projected_inflation = data['projected_inflation']
        if 'initial_goal_value' in data:
            goal.initial_goal_value = data['initial_goal_value']
        
        # Handle asset mappings if provided
        if 'asset_mappings' in data:
            try:
                validate_asset_mappings(data['asset_mappings'])
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
            
            # Remove existing mappings
            AssetGoalMapping.query.filter_by(goal_id=goal.id).delete()
            
            # Create new mappings
            for mapping in data['asset_mappings']:
                asset = Asset.query.get(mapping['asset_id'])
                if not asset:
                    return jsonify({'error': f"Asset not found with id: {mapping['asset_id']}"}), 404
                
                asset_goal_mapping = AssetGoalMapping(
                    goal=goal,
                    asset=asset,
                    allocation_percentage=mapping['allocation_percentage']
                )
                db.session.add(asset_goal_mapping)
        
        db.session.commit()
        return jsonify({
            'message': 'Goal updated successfully',
            'goal': goal.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['DELETE'])
def delete_goal(id):
    goal = Goal.query.get_or_404(id)
    db.session.delete(goal)
    db.session.commit()
    return jsonify({'message': 'Goal deleted successfully'}) 