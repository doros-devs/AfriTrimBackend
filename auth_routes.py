from flask_restx import Namespace, Resource
from auth_middleware import verify_token

# Define Namespace
auth_ns = Namespace('auth', description='Authentication related operations')

# Routes
@auth_ns.route('/verify')
class VerifyUser(Resource):
    @auth_ns.doc('verify_user', description="Endpoint to verify the user's token and provide role information.")
    @verify_token
    def post(self, decoded_token, decoded_token_roles):
        try:
            # Extract relevant information from the decoded token
            uid = decoded_token.get('uid')

            # Prepare response data with user roles
            response_data = {
                'uid': uid,
                'roles': decoded_token_roles
            }
            return response_data, 200
        except Exception as e:
            return {'error': 'Failed to verify token', 'message': str(e)}, 400
