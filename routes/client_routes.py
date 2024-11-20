from flask_restx import Namespace, Resource, fields
from services.client_service import get_barbershops, get_barbershop_details, create_appointment, update_appointment, \
    get_services_by_barbershop, update_client, delete_client, get_client_by_id, create_client
from flask import request

# Define Namespace
client_ns = Namespace('clients', description='Client related operations')

# Define Swagger models for request validation
appointment_model = client_ns.model('Appointment', {
    'client_name': fields.String(required=True, description='Client name'),
    'barber_id': fields.Integer(required=True, description='Barber ID'),
    'service_id': fields.Integer(required=True, description='Service ID'),
    'appointment_time': fields.String(required=True, description='Appointment time')
})

update_appointment_model = client_ns.model('UpdateAppointment', {
    'barber_id': fields.Integer(required=True, description='Barber ID'),
    'service_id': fields.Integer(required=True, description='Service ID'),
    'appointment_time': fields.String(required=True, description='Appointment time')
})

client_model = client_ns.model('Client', {
    'uid': fields.String(required=True, description='Firebase UID'),
    'name': fields.String(required=True, description='Client name'),
    'email': fields.String(required=True, description='Client email'),
    'phone_number': fields.String(description='Phone number'),
    'photo_url': fields.String(description='Profile picture URL')
})

# Routes
# Routes
@client_ns.route('/')
class ClientList(Resource):
    @client_ns.expect(client_model)
    @client_ns.doc('create_client')
    def post(self):
        """
        Create a new client
        """
        data = request.get_json()
        client = create_client(data)
        return client.to_dict(), 201

@client_ns.route('/<int:client_id>')
class Client(Resource):
    @client_ns.doc('get_client_by_id')
    def get(self, client_id):
        """
        Get client details by ID
        """
        client = get_client_by_id(client_id)
        if client:
            return client.to_dict(), 200
        return {'error': 'Client not found'}, 404

    @client_ns.expect(client_model)
    @client_ns.doc('update_client')
    def put(self, client_id):
        """
        Update client details by ID
        """
        data = request.get_json()
        client = update_client(client_id, data)
        if client:
            return client.to_dict(), 200
        return {'error': 'Client not found'}, 404

    @client_ns.doc('delete_client')
    def delete(self, client_id):
        """
        Delete client by ID
        """
        if delete_client(client_id):
            return {'message': 'Client deleted successfully'}, 200
        return {'error': 'Client not found'}, 404

@client_ns.route('/barbershops')
class BarbershopList(Resource):
    @client_ns.doc('get_barbershops')
    def get(self):
        """
        List all barbershops
        """
        barbershops = get_barbershops()
        return [{'id': shop.id, 'name': shop.name, 'location': shop.location} for shop in barbershops], 200


@client_ns.route('/barbershop/<int:barbershop_id>')
class BarbershopDetail(Resource):
    @client_ns.doc('get_barbershop_details')
    def get(self, barbershop_id):
        """
        Get details of a specific barbershop
        """
        barbershop = get_barbershop_details(barbershop_id)
        if barbershop:
            return {'id': barbershop.id, 'name': barbershop.name, 'location': barbershop.location}, 200
        return {'error': 'Barbershop not found'}, 404


@client_ns.route('/appointment')
class Appointment(Resource):
    @client_ns.expect(appointment_model)
    @client_ns.doc('create_appointment')
    def post(self):
        """
        Create a new appointment
        """
        data = request.get_json()
        appointment = create_appointment(
            client_id=data.get('client_id'),
            barber_id=data.get('barber_id'),
            service_id=data.get('service_id'),
            appointment_time=data.get('appointment_time')
        )
        return appointment.to_dict(), 201

@client_ns.route('/appointment/<int:appointment_id>')
class UpdateAppointment(Resource):
    @client_ns.expect(update_appointment_model)
    @client_ns.doc('update_appointment')
    def put(self, appointment_id):
        """
        Update an existing appointment
        """
        data = request.get_json()
        updated_appointment = update_appointment(
            appointment_id,
            barber_id=data.get('barber_id'),
            service_id=data.get('service_id'),
            appointment_time=data.get('appointment_time')
        )
        if updated_appointment:
            return updated_appointment.to_dict(), 200
        return {'error': 'Appointment not found'}, 404


@client_ns.route('/barbershop/<int:barbershop_id>/services')
class BarbershopServices(Resource):
    @client_ns.doc('get_services_by_barbershop')
    def get(self, barbershop_id):
        """
        Get all services offered by a specific barbershop
        """
        services = get_services_by_barbershop(barbershop_id)
        return [service.to_dict() for service in services], 200
