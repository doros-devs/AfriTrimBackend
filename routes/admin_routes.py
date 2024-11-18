from flask_restx import Namespace, Resource, fields
from flask import request
from auth_middleware import admin_required
from services.admin_service import (
    get_all_barbershops, update_payment_status, manage_barbershop,
    manage_barber, manage_service, manage_appointment,
    manage_invoice, manage_sale, manage_client_review, manage_client
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
@admin_ns.route('/barbershops')
class BarbershopList(Resource):
    @admin_ns.doc('get_all_barbershops')
    @admin_required
    def get(self):
        """
        List all barbershops
        """
        barbershops = get_all_barbershops()
        return [{'id': shop.id, 'name': shop.name, 'location': shop.location} for shop in barbershops], 200

@admin_ns.route('/payment/<string:admin_id>')
class PaymentStatus(Resource):
    @admin_ns.expect(payment_model)
    @admin_required
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
    @admin_required
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
    @admin_required
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
    @admin_required
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
    @admin_required
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
    @admin_required
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
    @admin_required
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
    @admin_required
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
    @admin_required
    def put(self, client_id):
        """
        Manage client
        """
        data = request.get_json()
        client = manage_client(client_id, data)
        if client:
            return client.to_dict(), 200
        return {'error': 'Client not found'}, 404
