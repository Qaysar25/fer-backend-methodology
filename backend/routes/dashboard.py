from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.stats_service import StatsService

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """
    Get Global Dashboard Statistics
    ---
    tags:
      - Dashboard
    security:
      - bearerAuth: []
    responses:
      200:
        description: Dashboard stats retrieved successfully
      401:
        description: Unauthorized
    """
    stats = StatsService.get_dashboard_stats()
    return jsonify(stats), 200

@dashboard_bp.route('/user-stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """
    Get User-Specific Statistics
    ---
    tags:
      - Dashboard
    security:
      - bearerAuth: []
    responses:
      200:
        description: User stats retrieved successfully
      401:
        description: Unauthorized
    """
    user_id = get_jwt_identity()
    stats = StatsService.get_user_stats(user_id)
    return jsonify(stats), 200
