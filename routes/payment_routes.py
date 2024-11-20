from flask import request
from flask_restx import Namespace, Resource, fields
from services.payment_service import (
    get_all_payments, create_payment, delete_payment,
    update_payment, get_payments_by_invoice, get_payments_by_sale
)

# Create Namespace for the payment routes
payment_ns = Namespace('payments', description='Operations related to payments')

# Define Swagger models for request validation
payment_model = payment_ns.model('Payment', {
    'admin_id': fields.String(required=True, description='Admin ID associated with the payment'),
    'amount': fields.Float(required=True, description='Payment amount'),
    'status': fields.String(required=False, description='Payment status'),
    'invoice_id': fields.Integer(required=False, description='Invoice ID associated with the payment'),
    'sale_id': fields.Integer(required=False, description='Sale ID associated with the payment')
})

# PAYMENT ROUTES
@payment_ns.route('/')
class PaymentList(Resource):
    @payment_ns.doc('get_all_payments')
    def get(self):
        """
        Get all payments
        """
        payments = get_all_payments()
        return [payment.to_dict() for payment in payments], 200

    @payment_ns.expect(payment_model)
    @payment_ns.doc('create_payment')
    def post(self):
        """
        Create a new payment
        """
        data = request.get_json()
        try:
            payment = create_payment(data)
            return payment.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@payment_ns.route('/<int:payment_id>')
class Payment(Resource):
    @payment_ns.doc('delete_payment')
    def delete(self, payment_id):
        """
        Delete a payment by ID
        """
        payment = delete_payment(payment_id)
        if payment:
            return {'message': 'Payment deleted successfully'}, 200
        return {'error': 'Payment not found'}, 404

    @payment_ns.expect(payment_model)
    @payment_ns.doc('update_payment')
    def put(self, payment_id):
        """
        Update a payment by ID
        """
        data = request.get_json()
        payment = update_payment(payment_id, data)
        if payment:
            return payment.to_dict(), 200
        return {'error': 'Payment not found'}, 404


@payment_ns.route('/invoice/<int:invoice_id>')
class PaymentsByInvoice(Resource):
    @payment_ns.doc('get_payments_by_invoice')
    def get(self, invoice_id):
        """
        Get all payments by invoice ID
        """
        payments = get_payments_by_invoice(invoice_id)
        if payments:
            return [payment.to_dict() for payment in payments], 200
        return {'error': 'No payments found for this invoice'}, 404


@payment_ns.route('/sale/<int:sale_id>')
class PaymentsBySale(Resource):
    @payment_ns.doc('get_payments_by_sale')
    def get(self, sale_id):
        """
        Get all payments by sale ID
        """
        payments = get_payments_by_sale(sale_id)
        if payments:
            return [payment.to_dict() for payment in payments], 200
        return {'error': 'No payments found for this sale'}, 404
