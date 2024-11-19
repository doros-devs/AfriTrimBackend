import os
import firebase_admin
from firebase_admin import credentials, storage, auth

def initialize_firebase(app):
    # Check if we are in a development or production environment
    flask_env = os.getenv('FLASK_ENV', 'production')

    if flask_env == 'development':
        # Load credentials from the service account file for development
        service_account_path = 'config/credentials/serviceAccountKey.json'
        cred = credentials.Certificate(service_account_path)
    else:
        # Load credentials from environment variables for production
        cred_dict = {
            "type": os.getenv('FIREBASE_TYPE', 'service_account'),
            "project_id": os.getenv('FIREBASE_PROJECT_ID'),
            "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
            "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
            "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
            "client_id": os.getenv('FIREBASE_CLIENT_ID'),
            "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
            "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
            "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
            "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL'),
        }

        # Check that all required fields are available
        if not all(cred_dict.values()):
            raise ValueError("One or more Firebase credential environment variables are not set.")

        # Initialize Firebase with the credentials
        cred = credentials.Certificate(cred_dict)

    # Initialize Firebase only if it hasn't been initialized already
    try:
        firebase_admin.get_app()
    except ValueError:
        # If no app has been initialized yet, do so here
        firebase_admin.initialize_app(cred, {
            'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET', 'afritrim-b1a83.appspot.com')
        })

    # Attach Firebase Storage bucket to app config
    app.config['FIREBASE_STORAGE_BUCKET'] = storage.bucket()



def set_custom_claims(user_uid, claims):
    """
    Set custom claims for a user.

    :param user_uid: Firebase user UID
    :param claims: Dictionary of custom claims (e.g., {"admin": True})
    """
    try:
        auth.set_custom_user_claims(user_uid, claims)
        print(f"Custom claims {claims} set for user {user_uid}")
    except Exception as e:
        print(f"Error setting custom claims for user {user_uid}: {e}")
