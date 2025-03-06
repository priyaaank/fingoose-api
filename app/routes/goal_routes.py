from flask import Blueprint, request, jsonify
from ..models.goal import Goal
from ..database import db
import re

bp = Blueprint('goals', __name__, url_prefix='/api/goals', static_folder=None)

def parse_month_year(date_str):
    """Parse date string in format 'YYYY-MM' and return month and year"""
    pattern = r'^(\d{4})-(\d{2})$'
    match = re.match(pattern, date_str)
    if not match:
        raise ValueError("Date must be in format 'YYYY-MM'")
    year, month = map(int, match.groups())
    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12")
    return month, year

@bp.route('', methods=['POST'])
def create_goal():
    data = request.get_json()
    
    try:
        month, year = parse_month_year(data['target_date'])
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    goal = Goal(
        type=data['type'],
        name=data['name'],
        target_amount=data['target_amount'],
        current_value=data['current_value'],
        target_month=month,
        target_year=year,
        expected_inflation=data['expected_inflation']
    )
    
    db.session.add(goal)
    db.session.commit()
    
    return jsonify({
        'id': goal.id,
        'message': 'Goal created successfully'
    }), 201

@bp.route('', methods=['GET'])
def get_goals():
    goals = Goal.query.all()
    return jsonify([{
        'id': goal.id,
        'type': goal.type,
        'name': goal.name,
        'target_amount': goal.target_amount,
        'current_value': goal.current_value,
        'target_date': f"{goal.target_year}-{goal.target_month:02d}",
        'expected_inflation': goal.expected_inflation
    } for goal in goals])

@bp.route('/<int:id>', methods=['GET'])
def get_goal(id):
    goal = Goal.query.get_or_404(id)
    return jsonify({
        'id': goal.id,
        'type': goal.type,
        'name': goal.name,
        'target_amount': goal.target_amount,
        'current_value': goal.current_value,
        'target_date': f"{goal.target_year}-{goal.target_month:02d}",
        'expected_inflation': goal.expected_inflation
    })

@bp.route('/<int:id>', methods=['PUT'])
def update_goal(id):
    goal = Goal.query.get_or_404(id)
    data = request.get_json()
    
    goal.type = data.get('type', goal.type)
    goal.name = data.get('name', goal.name)
    goal.target_amount = data.get('target_amount', goal.target_amount)
    goal.current_value = data.get('current_value', goal.current_value)
    if 'target_date' in data:
        try:
            month, year = parse_month_year(data['target_date'])
            goal.target_month = month
            goal.target_year = year
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    goal.expected_inflation = data.get('expected_inflation', goal.expected_inflation)
    
    db.session.commit()
    return jsonify({'message': 'Goal updated successfully'})

@bp.route('/<int:id>', methods=['DELETE'])
def delete_goal(id):
    goal = Goal.query.get_or_404(id)
    db.session.delete(goal)
    db.session.commit()
    return jsonify({'message': 'Goal deleted successfully'}) 