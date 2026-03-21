from flask import Blueprint, jsonify
from models.cnn_model import cnn_model

model_bp = Blueprint('model', __name__, url_prefix='/api/model')

@model_bp.route('/accuracy', methods=['GET'])
def get_accuracy():
    """
    Get Model Accuracy and Training Status
    ---
    tags:
      - Model
    responses:
      200:
        description: Model status and accuracy (NFR2 Compliant)
    """
    return jsonify({
        "accuracy": f"{int(cnn_model.accuracy * 100)}%",
        "status": "trained" if cnn_model.is_loaded else "mock_mode",
        "nfr_compliance": "NFR2"
    }), 200
