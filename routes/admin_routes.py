from datetime import datetime

from flask_restx import Namespace, Resource, fields
from flask import request
from app import db
from models import Barbershop, Service, Barber, Invoice
from services.admin_service import (
    get_all_barbershops, update_payment_status, manage_barbershop,
    manage_barber, manage_service, manage_appointment,
    manage_invoice, manage_sale, manage_client_review, manage_client, delete_admin, suspend_admin, get_admin_by_id,
)

# Define Namespace
admin_ns = Namespace('admin', description='Admin related operations')

# Define Swagger models for request validation
payment_model = admin_ns.model('Payment', {
    'status': fields.String(required=True, description='Payment status')
})

barbershop_model = admin_ns.model('Barbershop', {
    'name': fields.String(description='Barbershop name'),
    'location': fields.String(description='Barbershop location')
})

barber_model = admin_ns.model('Barber', {
    'name': fields.String(description='Barber name'),
    'available': fields.Boolean(description='Availability status')
})

service_model = admin_ns.model('Service', {
    'name': fields.String(description='Service name'),
    'price': fields.Float(description='Service price')
})

appointment_model = admin_ns.model('Appointment', {
    'appointment_time': fields.String(description='Appointment time')
})

invoice_model = admin_ns.model('Invoice', {
    'amount': fields.Float(description='Invoice amount'),
    'status': fields.String(description='Invoice status')
})

sale_model = admin_ns.model('Sale', {
    'barbershop_id': fields.Integer(description='Barbershop ID'),
    'barber_id': fields.Integer(description='Barber ID'),
    'client_id': fields.Integer(description='Client ID')
})

review_model = admin_ns.model('Review', {
    'rating': fields.Integer(description='Review rating'),
    'comment': fields.String(description='Review comment')
})

client_model = admin_ns.model('Client', {
    'name': fields.String(description='Client name'),
    'email': fields.String(description='Client email'),
    'phone_number': fields.String(description='Client phone number')
})

# Routes
# @admin_ns.route('/')
# class AdminList(Resource):
#     @admin_ns.expect(client_model)
#     @admin_ns.doc('create_admin')
#     def post(self):
#         """
#         Create a new admin user
#         """
#         data = request.get_json()
#         admin = create_admin(data)
#         return admin.to_dict(), 201

@admin_ns.route('/<int:admin_id>')
class Admin(Resource):
    @admin_ns.doc('get_admin_by_id')
    def get(self, admin_id):
        """
        Get an admin by ID
        """
        admin = get_admin_by_id(admin_id)
        if admin:
            return admin.to_dict(), 200
        return {'error': 'Admin not found'}, 404

    @admin_ns.doc('delete_admin')
    def delete(self, admin_id):
        """
        Delete an admin by ID
        """
        if delete_admin(admin_id):
            return {'message': 'Admin deleted successfully'}, 200
        return {'error': 'Admin not found'}, 404

@admin_ns.route('/suspend/<int:admin_id>')
class SuspendAdmin(Resource):
    @admin_ns.doc('suspend_admin')
    def put(self, admin_id):
        """
        Suspend an admin account by ID
        """
        admin = suspend_admin(admin_id)
        if admin:
            return {'message': 'Admin suspended successfully'}, 200
        return {'error': 'Admin not found'}, 404


@admin_ns.route('/barbershops')
class BarbershopList(Resource):
    @admin_ns.doc('get_all_barbershops')
    def get(self):
        """
        List all barbershops
        """
        barbershops = get_all_barbershops()
        return [{'id': shop.id, 'name': shop.name, 'location': shop.location} for shop in barbershops], 200

@admin_ns.route('/payment/<string:admin_id>')
class PaymentStatus(Resource):
    @admin_ns.expect(payment_model)
    def patch(self, admin_id):
        """
        Update payment status
        """
        data = request.get_json()
        status = data.get('status')
        payment = update_payment_status(admin_id, status)
        if payment:
            return payment.to_dict(), 200
        return {'error': 'Payment not found'}, 404

@admin_ns.route('/barbershop/<int:barbershop_id>')
class ManageBarbershop(Resource):
    @admin_ns.expect(barbershop_model)
    def put(self, barbershop_id):
        """
        Manage barbershop
        """
        data = request.get_json()
        barbershop = manage_barbershop(barbershop_id, data)
        if barbershop:
            return barbershop.to_dict(), 200
        return {'error': 'Barbershop not found'}, 404

@admin_ns.route('/barber/<int:barber_id>')
class ManageBarber(Resource):
    @admin_ns.expect(barber_model)
    def put(self, barber_id):
        """
        Manage barber
        """
        data = request.get_json()
        barber = manage_barber(barber_id, data)
        if barber:
            return barber.to_dict(), 200
        return {'error': 'Barber not found'}, 404

@admin_ns.route('/service/<int:service_id>')
class ManageService(Resource):
    @admin_ns.expect(service_model)
    def put(self, service_id):
        """
        Manage service
        """
        data = request.get_json()
        service = manage_service(service_id, data)
        if service:
            return service.to_dict(), 200
        return {'error': 'Service not found'}, 404

@admin_ns.route('/appointment/<int:appointment_id>')
class ManageAppointment(Resource):
    @admin_ns.expect(appointment_model)
    def put(self, appointment_id):
        """
        Manage appointment
        """
        data = request.get_json()
        appointment = manage_appointment(appointment_id, data)
        if appointment:
            return appointment.to_dict(), 200
        return {'error': 'Appointment not found'}, 404

@admin_ns.route('/invoice/<int:invoice_id>')
class ManageInvoice(Resource):
    @admin_ns.expect(invoice_model)
    def put(self, invoice_id):
        """
        Manage invoice
        """
        data = request.get_json()
        invoice = manage_invoice(invoice_id, data)
        if invoice:
            return invoice.to_dict(), 200
        return {'error': 'Invoice not found'}, 404

@admin_ns.route('/sale/<int:sale_id>')
class ManageSale(Resource):
    @admin_ns.expect(sale_model)
    def put(self, sale_id):
        """
        Manage sale
        """
        data = request.get_json()
        sale = manage_sale(sale_id, data)
        if sale:
            return sale.to_dict(), 200
        return {'error': 'Sale not found'}, 404

@admin_ns.route('/review/<int:review_id>')
class ManageClientReview(Resource):
    @admin_ns.expect(review_model)
    def put(self, review_id):
        """
        Manage client review
        """
        data = request.get_json()
        review = manage_client_review(review_id, data)
        if review:
            return review.to_dict(), 200
        return {'error': 'Review not found'}, 404

@admin_ns.route('/client/<int:client_id>')
class ManageClient(Resource):
    @admin_ns.expect(client_model)
    def put(self, client_id):
        """
        Manage client
        """
        data = request.get_json()
        client = manage_client(client_id, data)
        if client:
            return client.to_dict(), 200
        return {'error': 'Client not found'}, 404

@admin_ns.route('/<int:admin_id>')
class ManageAdmin(Resource):
    @admin_ns.expect(admin_ns.model('AdminPartialUpdate', {
        'is_active': fields.Boolean(description='Admin active status')
    }))
    def patch(self, admin_id):
        """
        Partially update an admin (e.g., suspend or activate)
        """
        data = request.get_json()
        admin = manage_client(admin_id, data)
        if admin:
            return admin.to_dict(), 200
        return {'error': 'Admin not found'}, 404

@admin_ns.route('/barbershop/<int:barbershop_id>')
class DeleteBarbershop(Resource):
    @admin_ns.doc('delete_barbershop')
    def delete(self, barbershop_id):
        """
        Delete a barbershop by ID
        """
        barbershop = Barbershop.query.get(barbershop_id)
        if barbershop:
            db.session.delete(barbershop)
            db.session.commit()
            return {'message': 'Barbershop deleted successfully'}, 200
        return {'error': 'Barbershop not found'}, 404

@admin_ns.route('/service/<int:service_id>')
class DeleteService(Resource):
    @admin_ns.doc('delete_service')
    def delete(self, service_id):
        """
        Delete a service by ID
        """
        service = Service.query.get(service_id)
        if service:
            db.session.delete(service)
            db.session.commit()
            return {'message': 'Service deleted successfully'}, 200
        return {'error': 'Service not found'}, 404

@admin_ns.route('/barber/<int:barber_id>')
class DeleteBarber(Resource):
    @admin_ns.doc('delete_barber')
    def delete(self, barber_id):
        """
        Delete a barber by ID
        """
        barber = Barber.query.get(barber_id)
        if barber:
            db.session.delete(barber)
            db.session.commit()
            return {'message': 'Barber deleted successfully'}, 200
        return {'error': 'Barber not found'}, 404

@admin_ns.route('/invoice/<int:invoice_id>')
class DeleteInvoice(Resource):
    @admin_ns.doc('delete_invoice')
    def delete(self, invoice_id):
        """
        Delete an invoice by ID
        """
        invoice = Invoice.query.get(invoice_id)
        if invoice:
            db.session.delete(invoice)
            db.session.commit()
            return {'message': 'Invoice deleted successfully'}, 200
        return {'error': 'Invoice not found'}, 404

@admin_ns.route('/barbershop')
class CreateBarbershop(Resource):
    @admin_ns.expect(barbershop_model)
    def post(self):
        """
        Create a new barbershop
        """
        data = request.get_json()
        barbershop = Barbershop(
            name=data.get('name'),
            location=data.get('location'),
            created_at=datetime.now()
        )
        db.session.add(barbershop)
        db.session.commit()
        return barbershop.to_dict(), 201
