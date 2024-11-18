from flask_restx import Namespace, Resource, fields
from services.client_service import get_barbershops, get_barbershop_details, create_appointment, update_appointment, get_services_by_barbershop
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

# Routes
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
            client_name=data.get('client_name'),
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
