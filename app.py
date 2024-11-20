from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_restx import Api
from firebase_utils import initialize_firebase
from database import db

# Load environment variables from .env file
load_dotenv()

# Application factory function
def create_app():
    # Create the Flask app and initialize CORS
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Configure the app using the settings from config.py
    app.config.from_object('config.Config')

    # Initialize SQLAlchemy and migrations
    db.init_app(app)
    migrate = Migrate(app, db)

    # Initialize Firebase
    initialize_firebase(app)

    # Initialize Flask-Restx API for Swagger documentation
    api = Api(app, version='1.0', title='AfriTrim API',
              description='API for managing the AfriTrim platform')

    # Import and register namespaces
    from routes.barbershop_routes import barbershop_ns
    from routes.client_routes import client_ns
    from routes.admin_routes import admin_ns
    from routes.service_routes import service_ns
    from routes.upload_routes import upload_ns
    from routes.appointment_routes import appointment_ns
    from routes.sale_routes import sale_ns
    from routes.payment_routes import payment_ns
    from routes.invoice_routes import invoice_ns
    from routes.review_routes import review_ns
    from routes.barber_routes import barber_ns
    from auth_routes import auth_ns
    from routes.user_routes import user_ns

    # Register namespaces with the API
    api.add_namespace(barbershop_ns, path='/api/barbershop')
    api.add_namespace(client_ns, path='/api/client')
    api.add_namespace(admin_ns, path='/api/admin')
    api.add_namespace(service_ns, path='/api/service')
    api.add_namespace(upload_ns, path='/api/upload')
    api.add_namespace(appointment_ns, path='/api/appointment')
    api.add_namespace(sale_ns, path='/api/sale')
    api.add_namespace(payment_ns, path='/api/payment')
    api.add_namespace(invoice_ns, path='/api/invoice')
    api.add_namespace(review_ns, path='/api/review')
    api.add_namespace(barber_ns, path='/api/barber')
    api.add_namespace(auth_ns, path='/api/auth')
    api.add_namespace(user_ns, path='/api/users')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization, X-Requested-With')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    # Add a basic route to check if the server is running
    @app.route('/')
    def index():
        return jsonify(message="Welcome to the Barbershop API! Refer to /api for more information.")

    return app

# Run the application
if __name__ == '__main__':
    app = create_app()
    # Run the server
    app.run(host='0.0.0.0', port=5555)
