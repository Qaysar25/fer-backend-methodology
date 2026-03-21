from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models here to ensure they are registered with SQLAlchemy
from .models.user import User
from .models.image import Image
from .models.face import Face
from .models.emotion_result import EmotionResult
from .models.dashboard_stats import DashboardStats

def init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
    print("[DB] SQLAlchemy Database initialized with methodology models.")
