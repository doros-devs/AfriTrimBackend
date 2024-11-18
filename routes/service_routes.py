from flask import request
from flask_restx import Namespace, Resource, fields
from services.service_service import create_service, get_all_services, get_service_by_id, update_service, delete_service

# Define Namespace
service_ns = Namespace('services', description='Operations related to services')

# Define Swagger models for request validation
service_model = service_ns.model('Service', {
    'name': fields.String(required=True, description='Service name'),
    'price': fields.Float(required=True, description='Service price'),
    'barbershop_id': fields.Integer(required=True, description='Barbershop ID'),
    'photo_url': fields.String(description='URL of the service photo')
})

# Routes
@service_ns.route('/')
class ServiceList(Resource):
    @service_ns.expect(service_model)
    @service_ns.doc('create_service')
    def post(self):
        """
        Create a new service
        """
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        barbershop_id = data.get('barbershop_id')
        photo_url = data.get('photo_url')
        service = create_service(name, price, barbershop_id, photo_url)
        return service.to_dict(), 201

    @service_ns.doc('get_all_services')
    def get(self):
        """
        Get all services
        """
        services = get_all_services()
        return [service.to_dict() for service in services], 200


@service_ns.route('/<int:service_id>')
class Service(Resource):
    @service_ns.doc('get_service_by_id')
    def get(self, service_id):
        """
        Get a service by ID
        """
        service = get_service_by_id(service_id)
        if service:
            return service.to_dict(), 200
        return {'error': 'Service not found'}, 404

    @service_ns.expect(service_model)
    @service_ns.doc('update_service')
    def patch(self, service_id):
        """
        Update a service by ID
        """
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        photo_url = data.get('photo_url')
        service = update_service(service_id, name, price, photo_url)
        if service:
            return service.to_dict(), 200
        return {'error': 'Service not found'}, 404

    @service_ns.doc('delete_service')
    def delete(self, service_id):
        """
        Delete a service by ID
        """
        service = delete_service(service_id)
        if service:
            return {'message': 'Service deleted successfully'}, 200
        return {'error': 'Service not found'}, 404
