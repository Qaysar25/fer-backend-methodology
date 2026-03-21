from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta

bcrypt = Bcrypt()

def init_security(app):
    """Initialize security extensions."""
    bcrypt.init_app(app)

def hash_password(password):
    """Hash a password using bcrypt."""
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(hashed_password, password):
    """Check if a password matches its hash."""
    return bcrypt.check_password_hash(hashed_password, password)

def generate_token(user_id):
    """Generate a JWT access token for a user."""
    expires = timedelta(hours=24)
    return create_access_token(identity=str(user_id), expires_delta=expires)
