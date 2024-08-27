from flask import Blueprint, request, jsonify
from app.models import db, Team, User
from app.utils import decode_token

team_bp = Blueprint('team', __name__)

@team_bp.route('/team', methods=['GET'])
def get_team():
    token = request.headers.get('Authorization').split(" ")[1]
    user_id = decode_token(token)
    team_members = Team.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': member.id,
        'downline': User.query.get(member.downline_id).username,
        'joined_at': member.joined_at,
        'status': member.status
    } for member in team_members])

@team_bp.route('/team/add', methods=['POST'])
def add_team_member():
    token = request.headers.get('Authorization').split(" ")[1]
    user_id = decode_token(token)
    data = request.get_json()
    downline = User.query.filter_by(username=data['downline_username']).first()
    if downline:
        new_member = Team(
            user_id=user_id,
            downline_id=downline.id,
            status='Active'
        )
        db.session.add(new_member)
        db.session.commit()
        return jsonify({'message': 'Team member added successfully'}), 201
    return jsonify({'error': 'User not found'}), 404
