from flask_restx import Namespace, Resource, fields
from auth_middleware import verify_token

# Define Namespace
auth_ns = Namespace('auth', description='Authentication related operations')

# Define Swagger models for request validation
verify_model = auth_ns.model('Verify', {
    'Authorization': fields.String(required=True, description='Bearer token for authentication', example='Bearer <token>')
})

# Routes
@auth_ns.route('/auth/verify')
class VerifyUser(Resource):
    @auth_ns.expect(verify_model, validate=True)
    @auth_ns.doc('verify_user', description="Endpoint to verify the user's token and provide role information.")
    @verify_token
    def post(self, decoded_token):
        try:
            # Extract relevant information from the decoded token
            uid = decoded_token.get('uid')
            is_admin = decoded_token.get('admin', False)
            is_barber = decoded_token.get('barber', False)
            is_client = decoded_token.get('client', False)

            # Prepare response data with user roles
            response_data = {
                'uid': uid,
                'roles': {
                    'admin': is_admin,
                    'barber': is_barber,
                    'client': is_client
                }
            }
            return response_data, 200
        except Exception as e:
            return {'error': 'Failed to verify token', 'message': str(e)}, 400
