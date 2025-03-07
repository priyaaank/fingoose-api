from flask import Blueprint, request, jsonify
from ..models.goal import Goal
from ..database import db

bp = Blueprint('goals', __name__, url_prefix='/api/goals', static_folder=None)

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
    return jsonify([goal.to_dict() for goal in goals])

@bp.route('/<int:id>', methods=['GET'])
def get_goal(id):
    goal = Goal.query.get_or_404(id)
    return jsonify(goal.to_dict())

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