import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Upload configuration
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database configuration
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'database', 'fer_database.db')}")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Security configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'default-key-for-dev')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-jwt-key')

# Model configuration (Methodology compliant)
MODEL_PATH = os.path.join(BASE_DIR, os.getenv('MODEL_PATH', 'models/face_emotion_model.h5'))
PROCESSING_TIMEOUT = 3.0  # seconds (NFR1)

# Flask configuration
DEBUG = True
