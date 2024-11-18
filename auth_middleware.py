from firebase_admin import auth
from flask import request, jsonify
from functools import wraps

# Middleware function for general token verification
def verify_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header is None:
                return jsonify({"error": "Authentication failed", "message": "Missing Authorization header"}), 401

            # Extract token from the Authorization header
            token = auth_header.split("Bearer ")[1]
            decoded_token = auth.verify_id_token(token)
            request.user = decoded_token  # Store user info for later use
        except Exception as e:
            return jsonify({"error": "Authentication failed", "message": str(e)}), 401

        return func(*args, **kwargs)

    return wrapper

# Decorator function for admin-only routes
def admin_required(func):
    """Decorator to restrict access to admin-only routes."""
    def wrapper(*args, **kwargs):
        try:
            token = request.headers.get('Authorization').split("Bearer ")[1]
            decoded_token = auth.verify_id_token(token)

            # Check custom claim for admin rights
            if 'admin' in decoded_token and decoded_token['admin']:
                return func(*args, **kwargs)
            else:
                return jsonify({"error": "Unauthorized access, admin required"}), 403
        except Exception as e:
            return jsonify({"error": "Authentication failed", "message": str(e)}), 401

    wrapper.__name__ = func.__name__
    return wrapper
