from flask import request
from flask_restx import Namespace, Resource, fields
from services.image_service import upload_and_save_image, allowed_file
import os

# Define Namespace
upload_ns = Namespace('upload', description='Operations related to image upload')

# Define Swagger model for request validation
upload_model = upload_ns.model('Upload', {
    'model': fields.String(required=True, description='Model name to associate with image'),
    'model_id': fields.String(required=True, description='Model ID to associate with image')
})

@upload_ns.route('/upload_image')
class UploadImage(Resource):
    @upload_ns.doc('upload_image')
    @upload_ns.expect(upload_model, validate=False)
    def post(self):
        """API endpoint to upload an image and save its URL in SQLAlchemy."""
        # Validate request file
        if 'file' not in request.files:
            return {'error': 'No file part in the request'}, 400

        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return {'error': 'No selected file or unsupported file type'}, 400

        # Save the file temporarily to upload to Firebase
        local_file_path = os.path.join('/tmp', file.filename)
        try:
            file.save(local_file_path)

            # Get model type and ID from request
            model = request.form.get('model')
            model_id = request.form.get('model_id')

            # Validate model and ID
            if not model or not model_id:
                raise ValueError('Model and Model ID are required fields')

            # Upload image and save URL to the model
            saved_entity = upload_and_save_image(local_file_path, model, model_id)

            if saved_entity:
                return saved_entity.to_dict(), 201
            else:
                return {'error': 'Entity not found or unable to save image URL'}, 404
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f"Unexpected error: {str(e)}"}, 500
        finally:
            # Clean up the local file
            if os.path.exists(local_file_path):
                os.remove(local_file_path)
