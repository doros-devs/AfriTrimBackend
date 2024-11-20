from flask import request
from flask_restx import Namespace, Resource, fields
from services.sale_services import (
    create_sale, update_sale, delete_sale,
    get_total_sales, get_average_sale, get_all_sales
)


# Define Namespace
sale_ns = Namespace('sales', description='Operations related to sales')

# Define Swagger models for request validation
sale_model = sale_ns.model('Sale', {
    'client_id': fields.Integer(required=True, description='Client ID'),
    'barbershop_id': fields.Integer(required=True, description='Barbershop ID'),
    'invoice_id': fields.Integer(required=True, description='Invoice ID'),
    'amount': fields.Float(required=True, description='Amount for the sale'),
    'expense': fields.Float(required=True, description='Expense associated with the sale')
})

# SALE ROUTES
@sale_ns.route('/')
class SaleList(Resource):
    @sale_ns.doc('get_all_sales')
    def get(self):
        """
        Get all sales
        """
        sales = get_all_sales()
        return [sale.to_dict() for sale in sales], 200

    @sale_ns.expect(sale_model)
    @sale_ns.doc('create_sale')
    def post(self):
        """
        Create a new sale
        """
        data = request.get_json()
        sale = create_sale(data)
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
        sale = update_sale(sale_id, data)
        if sale:
            return sale.to_dict(), 200
        return {'error': 'Sale not found'}, 404

    @sale_ns.doc('delete_sale')
    def delete(self, sale_id):
        """
        Delete a sale by ID
        """
        sale = delete_sale(sale_id)
        if sale:
            return {'message': 'Sale deleted successfully'}, 200
        return {'error': 'Sale not found'}, 404

@sale_ns.route('/totals')
class SaleTotals(Resource):
    @sale_ns.doc('get_total_sales')
    def get(self):
        """
        Get total sales, expenses, and profit
        """
        totals = get_total_sales()
        return totals, 200

@sale_ns.route('/average')
class AverageSale(Resource):
    @sale_ns.doc('get_average_sale')
    def get(self):
        """
        Get the average sale amount
        """
        barbershop_id = request.args.get('barbershop_id', type=int)
        barber_id = request.args.get('barber_id', type=int)
        avg_sale = get_average_sale(barbershop_id=barbershop_id, barber_id=barber_id)
        return {'average_sale': avg_sale}, 200
