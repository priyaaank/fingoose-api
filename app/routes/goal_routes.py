from flask import Blueprint, request, jsonify
from ..models.goal import Goal
from ..database import db
from datetime import datetime
import math

bp = Blueprint('goals', __name__, url_prefix='/api/goals', static_folder=None)

def calculate_projected_value(initial_value, inflation_rate, creation_year, target_year):
    """
    Calculate projected value using compound interest formula
    Using July (month 7) for both years to get exact mid-year calculation
    """
    years = target_year - creation_year
    # Convert percentage to decimal
    rate = inflation_rate / 100
    return initial_value * math.pow(1 + rate, years)

@bp.route('', methods=['POST'])
def create_goal():
    data = request.get_json()
    
    goal = Goal(
        name=data['name'],
        icon=data['icon'],
        goal_creation_year=data['goal_creation_year'],
        target_year=data['target_year'],
        projected_inflation=data['projected_inflation'],
        initial_goal_value=data['initial_goal_value']
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
        'name': goal.name,
        'icon': goal.icon,
        'goal_creation_year': goal.goal_creation_year,
        'target_year': goal.target_year,
        'projected_inflation': goal.projected_inflation,
        'initial_goal_value': goal.initial_goal_value,
        'projected_value': calculate_projected_value(
            goal.initial_goal_value,
            goal.projected_inflation,
            goal.goal_creation_year,
            goal.target_year
        ),
        'created_at': goal.created_at.isoformat(),
        'updated_at': goal.updated_at.isoformat()
    } for goal in goals])

@bp.route('/<int:id>', methods=['GET'])
def get_goal(id):
    goal = Goal.query.get_or_404(id)
    return jsonify({
        'id': goal.id,
        'name': goal.name,
        'icon': goal.icon,
        'goal_creation_year': goal.goal_creation_year,
        'target_year': goal.target_year,
        'projected_inflation': goal.projected_inflation,
        'initial_goal_value': goal.initial_goal_value,
        'projected_value': calculate_projected_value(
            goal.initial_goal_value,
            goal.projected_inflation,
            goal.goal_creation_year,
            goal.target_year
        ),
        'created_at': goal.created_at.isoformat(),
        'updated_at': goal.updated_at.isoformat()
    })

@bp.route('/<int:id>', methods=['PUT'])
def update_goal(id):
    goal = Goal.query.get_or_404(id)
    data = request.get_json()
    
    goal.name = data.get('name', goal.name)
    goal.icon = data.get('icon', goal.icon)
    goal.goal_creation_year = data.get('goal_creation_year', goal.goal_creation_year)
    goal.target_year = data.get('target_year', goal.target_year)
    goal.projected_inflation = data.get('projected_inflation', goal.projected_inflation)
    goal.initial_goal_value = data.get('initial_goal_value', goal.initial_goal_value)
    
    db.session.commit()
    return jsonify({'message': 'Goal updated successfully'})

@bp.route('/<int:id>', methods=['DELETE'])
def delete_goal(id):
    goal = Goal.query.get_or_404(id)
    db.session.delete(goal)
    db.session.commit()
    return jsonify({'message': 'Goal deleted successfully'}) 