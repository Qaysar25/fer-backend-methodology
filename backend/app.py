from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger
import os

from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY, JWT_SECRET_KEY, DEBUG, MAX_CONTENT_LENGTH, MODEL_PATH
from database.db import init_db
from utils.security import init_security
from models.cnn_model import cnn_model

# Import Blueprints
from routes.auth import auth_bp
from routes.analyze import analyze_bp
from routes.history import history_bp
from routes.dashboard import dashboard_bp
from routes.model import model_bp

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

    # Initialize extensions
    CORS(app)
    JWTManager(app)
    init_db(app)
    init_security(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(analyze_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(model_bp)

    # Swagger Documentation
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs"
    }
    app.config['SWAGGER'] = {
        'title': 'FER Backend API',
        'uiversion': 3
    }
    Swagger(app, config=swagger_config)

    # Initialize model
    cnn_model.load_model(MODEL_PATH)
    # Save mock architecture for future training
    cnn_model.save_architecture(os.path.join(os.path.dirname(MODEL_PATH), 'architecture.json'))

    @app.route('/')
    def index():
        return jsonify({
            "name": "Facial Emotion Recognition API (Methodology Compliant)",
            "version": "1.1",
            "status": "online",
            "docs": "/api/docs"
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
