from flask import request
from flask_restx import Namespace, Resource, fields
from firebase_admin import auth
from services.user_service import create_user, get_user_by_uid, delete_user, update_user, update_user_role
import logging
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Define Namespace
user_ns = Namespace('users', description='User related operations')

# Define Swagger models for request validation
signup_validate_model = user_ns.model('SignupValidate', {
    'role': fields.String(required=True, description='Role of the user'),
    'name': fields.String(required=True, description='User name'),
    'email': fields.String(required=True, description='User email'),
})

signup_verify_model = user_ns.model('SignupVerify', {
    'token': fields.String(required=True, description='Firebase ID token'),
    'role': fields.String(required=True, description='Role of the user'),
    'name': fields.String(required=True, description='User name'),
    'email': fields.String(required=True, description='User email'),
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
@user_ns.route('/signup/validate')
class UserSignupValidate(Resource):
    @user_ns.expect(signup_validate_model)
    @user_ns.doc('handle_signup_validation')
    def post(self):
        """
        Validate user signup data
        """
        try:
            # Extract data from the request
            data = request.get_json()
            role = data.get('role')
            name = data.get('name')
            email = data.get('email')

            # Validate fields
            if not role or not name or not email:
                return {"error": "Missing required fields: role, name, email"}, 400

            return {"message": "Validation successful"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

@user_ns.route('/signup/verify')
class UserSignupVerify(Resource):
    @user_ns.expect(signup_verify_model)
    @user_ns.doc('handle_signup_verification')
    def post(self):
        """
        Verify Firebase user and create a user record in the backend database
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
            logging.debug(f"Received login data: {data}")

            token = data.get('token')

            # Validate required fields
            if not token:
                raise ValueError("Missing required field: token")

            # Verify Firebase ID token
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            logging.debug(f"Decoded Firebase token: {decoded_token}")

            # Check user role by looking into the relevant tables
            user, role = get_user_by_uid(uid)
            if user:
                logging.info(f"User login successful: {user.to_dict()}")
                return {"role": role, "name": user.name, "email": user.email}, 200

            return {"error": "User not found"}, 404

        except ValueError as ve:
            logging.error(f"Validation error during login: {ve}")
            return {"error": str(ve)}, 400
        except SQLAlchemyError as se:
            logging.error(f"Database error during login: {se}")
            return {"error": "Database error occurred"}, 500
        except Exception as e:
            logging.error(f"Unexpected error during login: {e}")
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
            logging.debug(f"Received update data for UID {uid}: {data}")

            user = update_user(uid, data)
            logging.info(f"User updated successfully: {user.to_dict()}")
            return {"message": "User updated successfully", "user": user.to_dict()}, 200
        except ValueError as ve:
            logging.error(f"Validation error during user update: {ve}")
            return {"error": str(ve)}, 400
        except SQLAlchemyError as se:
            logging.error(f"Database error during user update: {se}")
            return {"error": "Database error occurred"}, 500
        except Exception as e:
            logging.error(f"Unexpected error during user update: {e}")
            return {"error": str(e)}, 500

    @user_ns.doc('delete_user')
    def delete(self, uid):
        """
        Delete a user
        """
        try:
            delete_user(uid)
            logging.info(f"User with UID {uid} deleted successfully")
            return {"message": "User successfully deleted"}, 200
        except ValueError as ve:
            logging.error(f"Validation error during user deletion: {ve}")
            return {"error": str(ve)}, 400
        except SQLAlchemyError as se:
            logging.error(f"Database error during user deletion: {se}")
            return {"error": "Database error occurred"}, 500
        except Exception as e:
            logging.error(f"Unexpected error during user deletion: {e}")
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
            logging.debug(f"Received role update data for UID {uid}: {data}")

            new_role = data.get('new_role')
            if not new_role:
                raise ValueError("Missing required field: new_role")

            user = update_user_role(uid, new_role)
            logging.info(f"User role updated successfully: {user.to_dict()}")
            return {"message": "User role updated successfully", "user": user.to_dict()}, 200
        except ValueError as ve:
            logging.error(f"Validation error during role update: {ve}")
            return {"error": str(ve)}, 400
        except SQLAlchemyError as se:
            logging.error(f"Database error during role update: {se}")
            return {"error": "Database error occurred"}, 500
        except Exception as e:
            logging.error(f"Unexpected error during role update: {e}")
            return {"error": str(e)}, 500

