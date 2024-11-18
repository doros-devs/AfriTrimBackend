from flask import request
from flask_restx import Namespace, Resource, fields
from app import db
from models import Sale
from datetime import datetime

# Define Namespace
sale_ns = Namespace('sales', description='Operations related to sales')

# Define Swagger models for request validation
sale_model = sale_ns.model('Sale', {
    'customer_name': fields.String(required=True, description='Customer name'),
    'barbershop_id': fields.Integer(required=True, description='Barbershop ID'),
    'barber_id': fields.Integer(required=True, description='Barber ID'),
    'invoice_id': fields.Integer(required=True, description='Invoice ID')
})

# SALE ROUTES
@sale_ns.route('/')
class SaleList(Resource):
    @sale_ns.doc('get_all_sales')
    def get(self):
        """
        Get all sales
        """
        sales = Sale.query.all()
        return [sale.to_dict() for sale in sales], 200

    @sale_ns.expect(sale_model)
    @sale_ns.doc('create_sale')
    def post(self):
        """
        Create a new sale
        """
        data = request.get_json()
        sale = Sale(
            customer_name=data.get('customer_name'),
            barbershop_id=data.get('barbershop_id'),
            barber_id=data.get('barber_id'),
            invoice_id=data.get('invoice_id'),
            sale_date=datetime.now()
        )
        db.session.add(sale)
        db.session.commit()
        return sale.to_dict(), 201

@sale_ns.route('/<int:sale_id>')
class SaleResource(Resource):
    @sale_ns.doc('update_sale')
    @sale_ns.expect(sale_model)
    def put(self, sale_id):
        """
        Update a sale by ID
        """
        data = request.get_json()
        sale = Sale.query.get(sale_id)
        if sale:
            if 'customer_name' in data:
                sale.customer_name = data['customer_name']
            if 'barbershop_id' in data:
                sale.barbershop_id = data['barbershop_id']
            if 'barber_id' in data:
                sale.barber_id = data['barber_id']
            if 'invoice_id' in data:
                sale.invoice_id = data['invoice_id']
            db.session.commit()
            return sale.to_dict(), 200
        return {'error': 'Sale not found'}, 404

    @sale_ns.doc('delete_sale')
    def delete(self, sale_id):
        """
        Delete a sale by ID
        """
        sale = Sale.query.get(sale_id)
        if sale:
            db.session.delete(sale)
            db.session.commit()
            return {'message': 'Sale deleted successfully'}, 200
        return {'error': 'Sale not found'}, 404
