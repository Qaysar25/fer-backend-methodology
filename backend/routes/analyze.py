from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.image_utils import validate_image
from services.emotion_pipeline import process_image

analyze_bp = Blueprint('analyze', __name__, url_prefix='/api')

@analyze_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze():
    """
    Analyze Facial Emotion (Methodology Compliant)
    ---
    tags:
      - Analysis
    security:
      - bearerAuth: []
    parameters:
      - name: image
        in: formData
        type: file
        required: true
        description: Facial image (JPG, PNG, JPEG)
    responses:
      200:
        description: Analysis successful (multi-face support)
      400:
        description: Invalid image input
      401:
        description: Unauthorized
    """
    if 'image' not in request.files:
        return jsonify({"message": "No image uploaded"}), 400

    file = request.files['image']
    is_valid, error = validate_image(file)
    if not is_valid:
        return jsonify({"message": error}), 400

    user_id = get_jwt_identity()
    result = process_image(file, user_id=user_id)

    if result.get('status') == 'error':
        return jsonify(result), 400

    return jsonify(result), 200
