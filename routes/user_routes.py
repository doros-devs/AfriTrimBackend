from flask import request
from flask_restx import Namespace, Resource, fields
from firebase_admin import auth
from services.user_service import create_user, get_user_by_uid, delete_user, update_user, update_user_role

# Define Namespace
user_ns = Namespace('users', description='User related operations')

# Define Swagger models for request validation
signup_model = user_ns.model('Signup', {
    'token': fields.String(required=True, description='Firebase ID token'),
    'role': fields.String(required=True, description='Role of the user'),
    'name': fields.String(required=True, description='User name'),
    'email': fields.String(required=True, description='User email'),
    'phone_number': fields.String(description='Phone number (optional)')
})

login_model = user_ns.model('Login', {
    'token': fields.String(required=True, description='Firebase ID token')
})

update_user_model = user_ns.model('UpdateUser', {
    'name': fields.String(description='User name'),
    'email': fields.String(description='User email'),
    'phone_number': fields.String(description='Phone number')
})

update_role_model = user_ns.model('UpdateRole', {
    'new_role': fields.String(required=True, description='New role for the user')
})

# Routes
@user_ns.route('/signup')
class UserSignup(Resource):
    @user_ns.expect(signup_model)
    @user_ns.doc('handle_signup')
    def post(self):
        """
        Handle user signup
        """
        try:
            # Extract data from the request
            data = request.get_json()
            token = data.get('token')
            role = data.get('role')

            # Verify Firebase ID token
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']

            # Save user data based on role
            data['uid'] = uid
            user = create_user(data, role)
            return {"message": "User successfully registered", "user": user.to_dict()}, 201

        except Exception as e:
            return {"error": str(e)}, 500


@user_ns.route('/login')
class UserLogin(Resource):
    @user_ns.expect(login_model)
    @user_ns.doc('handle_login')
    def post(self):
        """
        Handle user login
        """
        try:
            # Extract data from the request
            data = request.get_json()
            token = data.get('token')

            # Verify Firebase ID token
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']

            # Check user role by looking into the relevant tables
            user, role = get_user_by_uid(uid)
            if user:
                return {"role": role, "name": user.name, "email": user.email}, 200

            return {"error": "User not found"}, 404

        except Exception as e:
            return {"error": str(e)}, 500


@user_ns.route('/<string:uid>')
class User(Resource):
    @user_ns.expect(update_user_model)
    @user_ns.doc('handle_update_user')
    def put(self, uid):
        """
        Update user details
        """
        try:
            data = request.get_json()
            user = update_user(uid, data)
            return {"message": "User updated successfully", "user": user.to_dict()}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @user_ns.doc('delete_user')
    def delete(self, uid):
        """
        Delete a user
        """
        try:
            delete_user(uid)
            return {"message": "User successfully deleted"}, 200
        except Exception as e:
            return {"error": str(e)}, 500


@user_ns.route('/role/<string:uid>')
class UserRole(Resource):
    @user_ns.expect(update_role_model)
    @user_ns.doc('handle_update_user_role')
    def patch(self, uid):
        """
        Update user role
        """
        try:
            data = request.get_json()
            new_role = data.get('new_role')
            user = update_user_role(uid, new_role)
            return {"message": "User role updated successfully", "user": user.to_dict()}, 200
        except Exception as e:
            return {"error": str(e)}, 500
