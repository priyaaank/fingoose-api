from flask import Blueprint, request, jsonify
from ..models.liability import Liability
from ..database import db
from datetime import datetime
import re

bp = Blueprint('liabilities', __name__, url_prefix='/api/liabilities', static_folder=None)

def parse_month_year(date_str):
    """Parse date string in format 'YYYY-MM' and return month and year"""
    if not date_str:
        return None
    pattern = r'^(\d{4})-(\d{2})$'
    match = re.match(pattern, date_str)
    if not match:
        raise ValueError("Date must be in format 'YYYY-MM'")
    year, month = map(int, match.groups())
    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12")
    return datetime.strptime(f"{year}-{month:02d}-01", '%Y-%m-%d').date()

@bp.route('/<int:id>', methods=['GET'])
def get_liability(id):
    liability = Liability.query.get_or_404(id)
    return jsonify({
        'id': liability.id,
        'type': liability.type,
        'name': liability.name,
        'icon': liability.icon,
        'borrowed_principle': liability.borrowed_principle,
        'current_outstanding': liability.current_outstanding,
        'rate_of_interest': liability.rate_of_interest,
        'emi': liability.emi,
        'remaining_tenure': liability.remaining_tenure,
        'total_tenure': liability.total_tenure,
        'start_date': liability.start_date.strftime('%Y-%m'),
        'additional_comments': liability.additional_comments
    })

@bp.route('', methods=['POST'])
def create_liability():
    data = request.get_json()
    
    try:
        start_date = parse_month_year(data['start_date'])
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    liability = Liability(
        type=data['type'],
        name=data['name'],
        icon=data.get('icon'),
        borrowed_principle=data['borrowed_principle'],
        current_outstanding=data['current_outstanding'],
        rate_of_interest=data['rate_of_interest'],
        emi=data['emi'],
        remaining_tenure=data['remaining_tenure'],
        total_tenure=data['total_tenure'],
        start_date=start_date,
        additional_comments=data.get('additional_comments')
    )
    
    db.session.add(liability)
    db.session.commit()
    
    return jsonify({
        'id': liability.id,
        'message': 'Liability created successfully'
    }), 201

@bp.route('', methods=['GET'])
def get_liabilities():
    liabilities = Liability.query.all()
    return jsonify([{
        'id': liability.id,
        'type': liability.type,
        'name': liability.name,
        'icon': liability.icon,
        'borrowed_principle': liability.borrowed_principle,
        'current_outstanding': liability.current_outstanding,
        'rate_of_interest': liability.rate_of_interest,
        'emi': liability.emi,
        'remaining_tenure': liability.remaining_tenure,
        'total_tenure': liability.total_tenure,
        'start_date': liability.start_date.strftime('%Y-%m'),
        'additional_comments': liability.additional_comments
    } for liability in liabilities])

@bp.route('/<int:id>', methods=['DELETE'])
def delete_liability(id):
    liability = Liability.query.get_or_404(id)
    db.session.delete(liability)
    db.session.commit()
    return jsonify({'message': 'Liability deleted successfully'})

@bp.route('/<int:id>', methods=['PUT'])
def update_liability(id):
    liability = Liability.query.get_or_404(id)
    data = request.get_json()
    
    # Validate business rules
    if 'borrowed_principle' in data and 'current_outstanding' in data:
        if data['current_outstanding'] > data['borrowed_principle']:
            return jsonify({
                'error': 'Current outstanding cannot exceed borrowed principle'
            }), 400
    elif 'current_outstanding' in data and data['current_outstanding'] > liability.borrowed_principle:
        return jsonify({
            'error': 'Current outstanding cannot exceed borrowed principle'
        }), 400
    
    if 'total_tenure' in data and 'remaining_tenure' in data:
        if data['remaining_tenure'] > data['total_tenure']:
            return jsonify({
                'error': 'Remaining tenure cannot exceed total tenure'
            }), 400
    elif 'remaining_tenure' in data and data['remaining_tenure'] > liability.total_tenure:
        return jsonify({
            'error': 'Remaining tenure cannot exceed total tenure'
        }), 400
    
    # Update fields if provided
    if 'type' in data:
        liability.type = data['type']
    if 'name' in data:
        liability.name = data['name']
    if 'icon' in data:
        liability.icon = data['icon']
    if 'borrowed_principle' in data:
        liability.borrowed_principle = data['borrowed_principle']
    if 'current_outstanding' in data:
        liability.current_outstanding = data['current_outstanding']
    if 'rate_of_interest' in data:
        liability.rate_of_interest = data['rate_of_interest']
    if 'emi' in data:
        liability.emi = data['emi']
    if 'remaining_tenure' in data:
        liability.remaining_tenure = data['remaining_tenure']
    if 'total_tenure' in data:
        liability.total_tenure = data['total_tenure']
    if 'start_date' in data:
        try:
            liability.start_date = parse_month_year(data['start_date'])
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    if 'additional_comments' in data:
        liability.additional_comments = data['additional_comments']
    
    db.session.commit()
    return jsonify({'message': 'Liability updated successfully'}) 