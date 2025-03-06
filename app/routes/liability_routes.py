from flask import Blueprint, request, jsonify
from ..models.liability import Liability
from ..database import db
from datetime import datetime

bp = Blueprint('liabilities', __name__, url_prefix='/api/liabilities')

@bp.route('/', methods=['POST'])
def create_liability():
    data = request.get_json()
    
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
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        additional_comments=data.get('additional_comments')
    )
    
    db.session.add(liability)
    db.session.commit()
    
    return jsonify({
        'id': liability.id,
        'message': 'Liability created successfully'
    }), 201

@bp.route('/', methods=['GET'])
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
        'start_date': liability.start_date.strftime('%Y-%m-%d'),
        'additional_comments': liability.additional_comments
    } for liability in liabilities]) 