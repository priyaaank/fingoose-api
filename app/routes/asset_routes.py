from flask import Blueprint, request, jsonify
from ..models.asset import Asset
from ..models.goal import Goal
from ..models.asset_goal_mapping import AssetGoalMapping
from ..database import db
import re

bp = Blueprint('assets', __name__, url_prefix='/api/assets', static_folder=None)

def parse_month_year(date_str):
    """Parse date string in format 'YYYY-MM' and return month and year"""
    if not date_str:
        return None, None
    pattern = r'^(\d{4})-(\d{2})$'
    match = re.match(pattern, date_str)
    if not match:
        raise ValueError("Date must be in format 'YYYY-MM'")
    year, month = map(int, match.groups())
    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12")
    return month, year

def validate_goal_mappings(goal_mappings):
    """Validate goal mappings data"""
    if not isinstance(goal_mappings, list):
        raise ValueError("goal_mappings must be a list")
    
    total_allocation = 0
    goal_ids = set()
    
    for mapping in goal_mappings:
        if not isinstance(mapping, dict):
            raise ValueError("Each mapping must be an object")
        
        if 'goal_id' not in mapping or 'allocation_percentage' not in mapping:
            raise ValueError("Each mapping must have goal_id and allocation_percentage")
        
        allocation = float(mapping['allocation_percentage'])
        if allocation <= 0 or allocation > 100:
            raise ValueError("Allocation percentage must be between 0 and 100")
        
        if mapping['goal_id'] in goal_ids:
            raise ValueError(f"Duplicate goal_id found: {mapping['goal_id']}")
        
        goal_ids.add(mapping['goal_id'])
        total_allocation += allocation
    
    if total_allocation > 100:
        raise ValueError("Total allocation percentage cannot exceed 100%")
    
    return True

@bp.route('/<int:id>', methods=['GET'])
def get_asset(id):
    asset = Asset.query.get_or_404(id)
    return jsonify(asset.to_dict())

@bp.route('', methods=['POST'])
def create_asset():
    data = request.get_json()
    
    try:
        month, year = parse_month_year(data.get('maturity_date'))
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    # Start database transaction
    try:
        # Create asset
        asset = Asset(
            type=data['type'],
            name=data['name'],
            icon=data.get('icon'),
            current_value=data['current_value'],
            projected_roi=data['projected_roi'],
            maturity_month=month,
            maturity_year=year,
            additional_comments=data.get('additional_comments')
        )
        
        db.session.add(asset)
        
        # Handle goal mappings if provided
        if 'goal_mappings' in data:
            try:
                validate_goal_mappings(data['goal_mappings'])
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
            
            for mapping in data['goal_mappings']:
                goal = Goal.query.get(mapping['goal_id'])
                if not goal:
                    return jsonify({'error': f"Goal not found with id: {mapping['goal_id']}"}), 404
                
                asset_goal_mapping = AssetGoalMapping(
                    asset=asset,
                    goal=goal,
                    allocation_percentage=mapping['allocation_percentage']
                )
                db.session.add(asset_goal_mapping)
        
        db.session.commit()
        
        return jsonify({
            'id': asset.id,
            'message': 'Asset created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('', methods=['GET'])
def get_assets():
    assets = Asset.query.all()
    return jsonify([{
        'id': asset.id,
        'type': asset.type,
        'name': asset.name,
        'icon': asset.icon,
        'current_value': asset.current_value,
        'projected_roi': asset.projected_roi,
        'maturity_date': f"{asset.maturity_year}-{asset.maturity_month:02d}" if asset.maturity_month and asset.maturity_year else None,
        'additional_comments': asset.additional_comments
    } for asset in assets])

@bp.route('/<int:id>', methods=['PUT'])
def update_asset(id):
    asset = Asset.query.get_or_404(id)
    data = request.get_json()
    
    try:
        # Update asset fields
        if 'maturity_date' in data:
            try:
                month, year = parse_month_year(data['maturity_date'])
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
            asset.maturity_month = month
            asset.maturity_year = year
        
        # Update other fields if provided
        if 'type' in data:
            asset.type = data['type']
        if 'name' in data:
            asset.name = data['name']
        if 'icon' in data:
            asset.icon = data['icon']
        if 'current_value' in data:
            asset.current_value = data['current_value']
        if 'projected_roi' in data:
            asset.projected_roi = data['projected_roi']
        if 'additional_comments' in data:
            asset.additional_comments = data['additional_comments']
        
        # Handle goal mappings if provided
        if 'goal_mappings' in data:
            try:
                validate_goal_mappings(data['goal_mappings'])
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
            
            # Remove existing mappings
            AssetGoalMapping.query.filter_by(asset_id=asset.id).delete()
            
            # Create new mappings
            for mapping in data['goal_mappings']:
                goal = Goal.query.get(mapping['goal_id'])
                if not goal:
                    return jsonify({'error': f"Goal not found with id: {mapping['goal_id']}"}), 404
                
                asset_goal_mapping = AssetGoalMapping(
                    asset=asset,
                    goal=goal,
                    allocation_percentage=mapping['allocation_percentage']
                )
                db.session.add(asset_goal_mapping)
        
        db.session.commit()
        return jsonify({'message': 'Asset updated successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['DELETE'])
def delete_asset(id):
    asset = Asset.query.get_or_404(id)
    db.session.delete(asset)
    db.session.commit()
    return jsonify({'message': 'Asset deleted successfully'}) 