from flask import request
from flask_restx import Namespace, Resource, fields
from services.image_service import upload_and_save_image
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
        if 'file' not in request.files:
            return {'error': 'No file part in the request'}, 400

        file = request.files['file']
        if file.filename == '':
            return {'error': 'No selected file'}, 400

        # Save the file temporarily to upload to Firebase
        local_file_path = os.path.join('/tmp', file.filename)
        file.save(local_file_path)

        # Get model type and ID from request
        model = request.form.get('model')
        model_id = request.form.get('model_id')

        # Upload image and save URL to the model
        saved_entity = upload_and_save_image(local_file_path, model, model_id)

        # Clean up the local file
        os.remove(local_file_path)

        if saved_entity:
            return saved_entity.to_dict(), 201
        else:
            return {'error': 'Entity not found or unable to save image URL'}, 404
