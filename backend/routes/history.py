from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db import EmotionResult, Face, Image

history_bp = Blueprint('history', __name__, url_prefix='/api')

@history_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    """
    Get Analysis History
    ---
    tags:
      - Analysis
    security:
      - bearerAuth: []
    responses:
      200:
        description: History retrieved successfully
        schema:
          type: array
          items:
            type: object
            properties:
              filename: {type: string}
              emotion: {type: string}
              confidence: {type: number}
              date: {type: string}
      401:
        description: Unauthorized
    """
    user_id = get_jwt_identity()

    # Query all results for the current user
    results = EmotionResult.query.join(Face).join(Image).filter(Image.user_id == user_id).all()

    history = [
        {
            "filename": r.face.image.filename,
            "emotion": r.emotion,
            "confidence": r.confidence_score,
            "date": r.analyzed_at.isoformat()
        }
        for r in results
    ]

    return jsonify(history), 200
