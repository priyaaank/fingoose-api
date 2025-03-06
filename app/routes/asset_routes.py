from flask import Blueprint, request, jsonify
from ..models.asset import Asset
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

@bp.route('', methods=['POST'])
def create_asset():
    data = request.get_json()
    
    try:
        month, year = parse_month_year(data.get('maturity_date'))
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
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
        'maturity_date': f"{asset.maturity_year}-{asset.maturity_month:02d}" if asset.maturity_month and asset.maturity_year else None,
        'additional_comments': asset.additional_comments
    } for asset in assets]) 