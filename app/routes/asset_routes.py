from flask import Blueprint, request, jsonify
from ..models.asset import Asset
from ..database import db
from datetime import datetime

bp = Blueprint('assets', __name__, url_prefix='/api/assets', static_folder=None)

@bp.route('', methods=['POST'])
def create_asset():
    data = request.get_json()
    
    asset = Asset(
        type=data['type'],
        name=data['name'],
        icon=data.get('icon'),
        current_value=data['current_value'],
        projected_roi=data['projected_roi'],
        maturity_date=datetime.strptime(data['maturity_date'], '%Y-%m-%d').date() if 'maturity_date' in data else None,
        additional_comments=data.get('additional_comments')
    )
    
    db.session.add(asset)
    db.session.commit()
    
    return jsonify({
        'id': asset.id,
        'message': 'Asset created successfully'
    }), 201

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
        'maturity_date': asset.maturity_date.strftime('%Y-%m-%d') if asset.maturity_date else None,
        'additional_comments': asset.additional_comments
    } for asset in assets]) 