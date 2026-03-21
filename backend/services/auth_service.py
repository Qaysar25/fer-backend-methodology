from database.db import db, User
from utils.security import hash_password, check_password, generate_token

def register_user(username, email, password, role='user'):
    """Register a new user in the database."""
    if User.query.filter_by(username=username).first():
        return None, "Username already exists."
    if User.query.filter_by(email=email).first():
        return None, "Email already exists."

    new_user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
        role=role
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user, None

def login_user(username, password):
    """Authenticate a user and return a token."""
    user = User.query.filter_by(username=username).first()
    if user and check_password(user.password_hash, password):
        token = generate_token(user.user_id)
        return token, user
    return None, "Invalid username or password."
