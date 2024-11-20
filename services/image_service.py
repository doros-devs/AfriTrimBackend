from firebase_admin import storage
from app import db
from models import Barbershop, Barber, Service
from sqlalchemy.exc import SQLAlchemyError

# Allowed models and extensions for validation
ALLOWED_MODELS = ['barbershop', 'barber', 'service']
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_model_and_id(model, model_id):
    if model not in ALLOWED_MODELS:
        raise ValueError(f"Invalid model provided: {model}")
    if not model_id.isdigit():
        raise ValueError(f"Invalid model_id provided: {model_id}")


# Function to upload image to Firebase Storage
def upload_image_to_storage(local_file_path, destination_path):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(destination_path)
        blob.upload_from_filename(local_file_path)
        blob.make_public()
        return blob.public_url
    except Exception as e:
        raise ValueError(f"Failed to upload image to Firebase Storage: {str(e)}")


# Function to update SQLAlchemy model with image URL
def save_image_url_to_sqlalchemy(model, model_id, image_url):
    try:
        if model == 'barbershop':
            entity = Barbershop.query.get(model_id)
        elif model == 'barber':
            entity = Barber.query.get(model_id)
        elif model == 'service':
            entity = Service.query.get(model_id)
        else:
            raise ValueError("Invalid model type")

        if entity:
            entity.photo_url = image_url
            db.session.commit()
            return entity
        else:
            raise ValueError(f"{model.capitalize()} with ID {model_id} not found")
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Failed to save image URL to database: {str(e)}")


# Main function to handle upload and saving image
def upload_and_save_image(local_file_path, model, model_id):
    try:
        # Validate model and ID
        validate_model_and_id(model, model_id)

        destination_path = f'images/{model}/{model_id}.jpg'
        image_url = upload_image_to_storage(local_file_path, destination_path)
        saved_entity = save_image_url_to_sqlalchemy(model, model_id, image_url)
        return saved_entity
    except ValueError as e:
        raise ValueError(f"Failed to upload and save image: {str(e)}")
