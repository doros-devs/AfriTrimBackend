from flask_restx import Namespace, Resource, fields
from flask import request
from services.barbershop_service import create_barbershop, add_barber_to_barbershop, add_service_to_barbershop, \
    schedule_barber, create_review, check_payment_status, get_all_barbershops, get_barbershop_by_id, update_barbershop, \
    delete_barbershop, search_barbershops, list_barbers_for_barbershop, list_services_for_barbershop

# Define Namespace
barbershop_ns = Namespace('barbershop', description='Operations related to barbershop')

# Define Swagger models for request validation
barbershop_model = barbershop_ns.model('Barbershop', {
    'admin_id': fields.String(required=True, description='Admin ID'),
    'name': fields.String(required=True, description='Barbershop name'),
    'location': fields.String(required=True, description='Barbershop location')
})

barber_model = barbershop_ns.model('Barber', {
    'name': fields.String(required=True, description='Barber name')
})

service_model = barbershop_ns.model('Service', {
    'name': fields.String(required=True, description='Service name'),
    'price': fields.Float(required=True, description='Service price')
})

availability_model = barbershop_ns.model('Availability', {
    'available': fields.Boolean(required=True, description='Availability status')
})

review_model = barbershop_ns.model('Review', {
    'rating': fields.Integer(required=True, description='Review rating'),
    'comment': fields.String(description='Review comment')
})

update_barbershop_model = barbershop_ns.model('UpdateBarbershop', {
    'name': fields.String(description='Barbershop name'),
    'location': fields.String(description='Barbershop location'),
    'photo_url': fields.String(description='URL of the barbershop photo')
})

# Routes
@barbershop_ns.route('/')
class CreateBarbershop(Resource):
    @barbershop_ns.expect(barbershop_model)
    @barbershop_ns.doc('create_barbershop')
    def post(self):
        """
        Create a new barbershop
        """
        data = request.get_json()
        admin_id = data.get('admin_id')  # Replaced 'owner_id' with 'admin_id'
        name = data.get('name')
        location = data.get('location')
        barbershop = create_barbershop(admin_id, name, location)  # Updated argument from 'owner_id' to 'admin_id'
        return {'id': barbershop.id}, 201

    @barbershop_ns.doc('get_all_barbershops')
    def get(self):
        """
        Get all barbershops
        """
        barbershops = get_all_barbershops()
        return [barbershop.to_dict() for barbershop in barbershops], 200

@barbershop_ns.route('/<int:barbershop_id>')
class GetBarbershop(Resource):
    @barbershop_ns.doc('get_barbershop_by_id')
    def get(self, barbershop_id):
        """
        Get a specific barbershop by ID
        """
        barbershop = get_barbershop_by_id(barbershop_id)
        return barbershop.to_dict(), 200

    @barbershop_ns.expect(update_barbershop_model)
    @barbershop_ns.doc('update_barbershop')
    def patch(self, barbershop_id):
        """
        Update a barbershop by ID
        """
        data = request.get_json()
        updated_barbershop = update_barbershop(barbershop_id, data)
        if updated_barbershop:
            return updated_barbershop.to_dict(), 200
        return {'error': 'Barbershop not found'}, 404

    @barbershop_ns.doc('delete_barbershop')
    def delete(self, barbershop_id):
        """
        Delete a barbershop by ID
        """
        deleted = delete_barbershop(barbershop_id)
        if deleted:
            return {'message': 'Barbershop deleted successfully'}, 200

@barbershop_ns.route('/<int:barbershop_id>/barbers')
class GetBarbersByBarbershop(Resource):
    @barbershop_ns.doc('get_barbers_by_barbershop')
    def get(self, barbershop_id):
        """
        Get all barbers associated with a specific barbershop
        """
        barbershop = get_barbershop_by_id(barbershop_id)
        return [barber.to_dict() for barber in barbershop.barbers], 200

@barbershop_ns.route('/<int:barbershop_id>/services')
class GetServicesByBarbershop(Resource):
    @barbershop_ns.doc('get_services_by_barbershop')
    def get(self, barbershop_id):
        """
        Get all services provided by a specific barbershop
        """
        barbershop = get_barbershop_by_id(barbershop_id)
        return [service.to_dict() for service in barbershop.services], 200

@barbershop_ns.route('/<int:barbershop_id>/barber')
class AddBarber(Resource):
    @barbershop_ns.expect(barber_model)
    @barbershop_ns.doc('add_barber_to_barbershop')
    def post(self, barbershop_id):
        """
        Add a barber to a barbershop
        """
        data = request.get_json()
        name = data.get('name')
        barber = add_barber_to_barbershop(barbershop_id, name)
        return {'id': barber.id}, 201


@barbershop_ns.route('/<int:barbershop_id>/service')
class AddService(Resource):
    @barbershop_ns.expect(service_model)
    @barbershop_ns.doc('add_service_to_barbershop')
    def post(self, barbershop_id):
        """
        Add a service to a barbershop
        """
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        service = add_service_to_barbershop(barbershop_id, name, price)
        return {'id': service.id}, 201


@barbershop_ns.route('/barber/<int:barber_id>/availability')
class ScheduleBarber(Resource):
    @barbershop_ns.expect(availability_model)
    @barbershop_ns.doc('schedule_barber')
    def patch(self, barber_id):
        """
        Schedule a barber's availability
        """
        data = request.get_json()
        available = data.get('available')
        barber = schedule_barber(barber_id, available)
        return {'available': barber.available}, 200


@barbershop_ns.route('/barber/<int:barber_id>/review')
class CreateReview(Resource):
    @barbershop_ns.expect(review_model)
    @barbershop_ns.doc('create_review')
    def post(self, barber_id):
        """
        Create a review for a barber
        """
        data = request.get_json()
        rating = data.get('rating')
        comment = data.get('comment')
        review = create_review(barber_id, rating, comment)
        return {'id': review.id}, 201


@barbershop_ns.route('/payment/<string:admin_id>')  # Replaced 'owner_id' with 'admin_id'
class CheckPaymentStatus(Resource):
    @barbershop_ns.doc('check_payment_status')
    def get(self, admin_id):
        """
        Check payment status for an admin
        """
        status = check_payment_status(admin_id)  # Updated argument from 'owner_id' to 'admin_id'
        return {'status': status}, 200

@barbershop_ns.route('/search')
class SearchBarbershop(Resource):
    @barbershop_ns.doc('search_barbershops')
    def get(self):
        """
        Search barbershops by name or location
        """
        query = request.args.get('query')
        barbershops = search_barbershops(query)
        return [barbershop.to_dict() for barbershop in barbershops], 200

@barbershop_ns.route('/<int:barbershop_id>/barbers')
class BarbersForBarbershop(Resource):
    @barbershop_ns.doc('list_barbers_for_barbershop')
    def get(self, barbershop_id):
        """
        List all barbers for a barbershop
        """
        barbers = list_barbers_for_barbershop(barbershop_id)
        return [barber.to_dict() for barber in barbers], 200


@barbershop_ns.route('/<int:barbershop_id>/services')
class ServicesForBarbershop(Resource):
    @barbershop_ns.doc('list_services_for_barbershop')
    def get(self, barbershop_id):
        """
        List all services for a barbershop
        """
        services = list_services_for_barbershop(barbershop_id)
        return [service.to_dict() for service in services], 200
