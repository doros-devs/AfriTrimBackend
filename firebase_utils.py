import os
import json
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import storage


import os
import json
import firebase_admin
from firebase_admin import credentials, storage

def initialize_firebase(app):
    # Check if we are in a development or production environment
    flask_env = os.getenv('FLASK_ENV', 'production')

    if flask_env == 'development':
        # Load credentials from the service account file for development
        service_account_path = 'config/credentials/serviceAccountKey.json'
        cred = credentials.Certificate(service_account_path)
    else:
        # Load credentials from environment variable for production
        service_account_info = os.getenv('FIREBASE_CREDENTIALS')

        if not service_account_info:
            raise ValueError("FIREBASE_CREDENTIALS environment variable not set.")

        # Convert the JSON string from the environment variable to a dictionary
        cred_dict = json.loads(service_account_info)
        cred = credentials.Certificate(cred_dict)

    # Initialize Firebase with the credentials
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
