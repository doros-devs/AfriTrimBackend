from flask import request
from flask_restx import Namespace, Resource, fields
from services.invoice_service import (
    create_invoice,
    get_invoice_by_id,
    get_all_invoices,
    update_invoice,
    delete_invoice,
    get_invoices_for_client,
    get_invoices_for_barbershop
)

# Define Namespace
invoice_ns = Namespace('invoices', description='Operations related to invoices')

# Define Swagger models for request validation
invoice_model = invoice_ns.model('Invoice', {
    'client_id': fields.Integer(required=True, description='Client ID'),
    'barbershop_id': fields.Integer(required=True, description='Barbershop ID'),
    'amount': fields.Float(required=True, description='Invoice amount'),
    'status': fields.String(description='Invoice status')
})

status_model = invoice_ns.model('Status', {
    'status': fields.String(required=True, description='New status of the invoice')
})

# Routes
@invoice_ns.route('/')
class InvoiceList(Resource):
    @invoice_ns.doc('get_all_invoices')
    def get(self):
        """
        Get all invoices.
        """
        invoices = get_all_invoices()
        return [invoice.to_dict() for invoice in invoices], 200

    @invoice_ns.expect(invoice_model)
    @invoice_ns.doc('create_invoice')
    def post(self):
        """
        Create a new invoice.
        """
        data = request.get_json()
        invoice = create_invoice(data)
        return invoice.to_dict(), 201

@invoice_ns.route('/<int:invoice_id>')
class Invoice(Resource):
    @invoice_ns.doc('get_invoice_by_id')
    def get(self, invoice_id):
        """
        Get an invoice by ID.
        """
        invoice = get_invoice_by_id(invoice_id)
        if invoice:
            return invoice.to_dict(), 200
        else:
            return {'error': 'Invoice not found'}, 404

    @invoice_ns.expect(invoice_model)
    @invoice_ns.doc('update_invoice')
    def put(self, invoice_id):
        """
        Update an invoice by ID.
        """
        data = request.get_json()
        updated_invoice = update_invoice(invoice_id, data)
        if updated_invoice:
            return updated_invoice.to_dict(), 200
        else:
            return {'error': 'Invoice not found or unable to update'}, 404

    @invoice_ns.doc('delete_invoice')
    def delete(self, invoice_id):
        """
        Delete an invoice by ID.
        """
        if delete_invoice(invoice_id):
            return {'message': 'Invoice deleted successfully'}, 200
        return {'error': 'Invoice not found'}, 404

@invoice_ns.route('/client/<int:client_id>')
@invoice_ns.param('client_id', 'The client identifier')
class ClientInvoices(Resource):
    @invoice_ns.doc('get_invoices_for_client')
    def get(self, client_id):
        """
        Get all invoices for a specific client.
        """
        invoices = get_invoices_for_client(client_id)
        return [invoice.to_dict() for invoice in invoices], 200

@invoice_ns.route('/barbershop/<int:barbershop_id>')
@invoice_ns.param('barbershop_id', 'The barbershop identifier')
class BarbershopInvoices(Resource):
    @invoice_ns.doc('get_invoices_for_barbershop')
    def get(self, barbershop_id):
        """
        Get all invoices for a specific barbershop.
        """
        invoices = get_invoices_for_barbershop(barbershop_id)
        return [invoice.to_dict() for invoice in invoices], 200
