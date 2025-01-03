from flask_restx import Namespace, Resource, fields
from flask import request
from services.appointment_services import (
    get_all_appointments,
    create_appointment,
    get_appointment_by_id,
    update_appointment,
    delete_appointment, get_upcoming_appointments_for_barber, update_appointment_status
)
from models import Appointment

# Define Namespace
appointment_ns = Namespace('appointments', description='Appointments related operations')

# Define Swagger models for request validation
appointment_model = appointment_ns.model('Appointment', {
    'client_id': fields.Integer(required=True, description='Client ID'),
    'barber_id': fields.Integer(required=True, description='Barber ID'),
    'service_id': fields.Integer(required=True, description='Service ID'),
    'appointment_time': fields.String(required=True, description='Appointment time (YYYY-MM-DD HH:MM:SS)')
})

# Routes
@appointment_ns.route('/')
class AppointmentList(Resource):
    @appointment_ns.doc('get_all_appointments')
    def get(self):
        """
        List all appointments
        """
        appointments = get_all_appointments()
        return [appointment.to_dict() for appointment in appointments], 200

    @appointment_ns.expect(appointment_model)
    @appointment_ns.doc('create_appointment')
    def post(self):
        """
        Create a new appointment
        """
        data = request.get_json()
        appointment = create_appointment(data)
        return appointment.to_dict(), 201

@appointment_ns.route('/<int:appointment_id>')
@appointment_ns.param('appointment_id', 'The appointment identifier')
class Appointment(Resource):
    @appointment_ns.doc('get_appointment')
    def get(self, appointment_id):
        """
        Get an appointment by ID
        """
        appointment = get_appointment_by_id(appointment_id)
        if appointment:
            return appointment.to_dict(), 200
        return {'error': 'Appointment not found'}, 404

    @appointment_ns.expect(appointment_model)
    @appointment_ns.doc('update_appointment')
    def put(self, appointment_id):
        """
        Update an appointment by ID
        """
        data = request.get_json()
        appointment = update_appointment(appointment_id, data)
        if appointment:
            return appointment.to_dict(), 200
        return {'error': 'Appointment not found'}, 404

    @appointment_ns.doc('delete_appointment')
    def delete(self, appointment_id):
        """
        Delete an appointment by ID
        """
        if delete_appointment(appointment_id):
            return {'message': 'Appointment deleted successfully'}, 200
        return {'error': 'Appointment not found'}, 404

@appointment_ns.route('/<int:appointment_id>/status')
@appointment_ns.param('appointment_id', 'The appointment identifier')
class AppointmentStatus(Resource):
    @appointment_ns.doc('update_appointment_status')
    @appointment_ns.expect(appointment_ns.model('UpdateStatus', {
        'status': fields.String(required=True, description='New status for the appointment')
    }))
    def put(self, appointment_id):
        """
        Update the status of an appointment by ID
        """
        data = request.get_json()
        status = data.get('status')
        if status not in ['Scheduled', 'Completed', 'Cancelled']:
            return {'error': 'Invalid status value'}, 400
        appointment = update_appointment_status(appointment_id, status)
        if appointment:
            return appointment.to_dict(), 200
        return {'error': 'Appointment not found'}, 404

@appointment_ns.route('/barber/<int:barber_id>/upcoming')
@appointment_ns.param('barber_id', 'The barber identifier')
class UpcomingAppointments(Resource):
    @appointment_ns.doc('get_upcoming_appointments_for_barber')
    def get(self, barber_id):
        """
        Get all upcoming appointments for a barber
        """
        appointments = get_upcoming_appointments_for_barber(barber_id)
        return [appointment.to_dict() for appointment in appointments], 200

@appointment_ns.route('/client/<int:client_id>')
@appointment_ns.param('client_id', 'The client identifier')
class ClientAppointments(Resource):
    @appointment_ns.doc('get_appointments_for_client')
    def get(self, client_id):
        """
        Get all appointments for a specific client
        """
        appointments = Appointment.query.filter_by(client_id=client_id).all()
        return [appointment.to_dict() for appointment in appointments], 200

@appointment_ns.route('/barber/<int:barber_id>')
@appointment_ns.param('barber_id', 'The barber identifier')
class BarberAppointments(Resource):
    @appointment_ns.doc('get_appointments_for_barber')
    def get(self, barber_id):
        """
        Get all appointments for a specific barber
        """
        appointments = Appointment.query.filter_by(barber_id=barber_id).all()
        return [appointment.to_dict() for appointment in appointments], 200
