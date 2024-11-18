from firebase_admin import storage
from app import db
from models import Barbershop, Barber, Service

# Function to upload image to Firebase Storage
def upload_image_to_storage(local_file_path, destination_path):
    bucket = storage.bucket()
    blob = bucket.blob(destination_path)
    blob.upload_from_filename(local_file_path)
    blob.make_public()
    return blob.public_url

# Function to update SQLAlchemy model with image URL
def save_image_url_to_sqlalchemy(model, model_id, image_url):
    if model == 'barbershop':
        barbershop = Barbershop.query.get(model_id)
        if barbershop:
            barbershop.photo_url = image_url
            db.session.commit()
            return barbershop
    elif model == 'barber':
        barber = Barber.query.get(model_id)
        if barber:
            barber.photo_url = image_url
            db.session.commit()
            return barber
    elif model == 'service':
        service = Service.query.get(model_id)
        if service:
            service.photo_url = image_url
            db.session.commit()
            return service
    return None

# Main function to handle upload and saving image
def upload_and_save_image(local_file_path, model, model_id):
    destination_path = f'images/{model}/{model_id}.jpg'
    image_url = upload_image_to_storage(local_file_path, destination_path)
    saved_entity = save_image_url_to_sqlalchemy(model, model_id, image_url)
    return saved_entity
