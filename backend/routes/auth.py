from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    User Registration
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username: {type: string}
            email: {type: string}
            password: {type: string}
    responses:
      201:
        description: User registered successfully
      400:
        description: Invalid data or user already exists
    """
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({"message": "Missing required fields"}), 400

    user, error = register_user(username, email, password)
    if error:
        return jsonify({"message": error}), 400

    return jsonify({
        "message": "User registered successfully",
        "user_id": user.user_id
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User Login
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username: {type: string}
            password: {type: string}
    responses:
      200:
        description: Login successful, returns token
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    token, user_or_error = login_user(username, password)
    if not token:
        return jsonify({"message": user_or_error}), 401

    return jsonify({
        "access_token": token,
        "username": user_or_error.username,
        "role": user_or_error.role
    }), 200
