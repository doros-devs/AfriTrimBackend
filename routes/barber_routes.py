from flask_restx import Namespace, Resource, fields
from flask import request
from services.barber_service import (
    get_all_barbers, get_barber_by_id, create_barber, update_barber, delete_barber, update_barber_availability,
    search_barbers_by_name, get_reviews_for_barber, get_barbers_by_availability, get_barbers_by_barbershop
)

# Define Namespace
barber_ns = Namespace('barbers', description='Operations related to barbers')

# Define Swagger models for request validation
barber_model = barber_ns.model('Barber', {
    'name': fields.String(required=True, description='Barber name'),
    'barbershop_id': fields.Integer(required=True, description='Barbershop ID'),
    'photo_url': fields.String(description="URL of the barber's photo")
})

availability_model = barber_ns.model('Availability', {
    'available': fields.Boolean(required=True, description='Availability status')
})

# Routes
@barber_ns.route('/')
class BarberList(Resource):
    @barber_ns.doc('get_all_barbers')
    def get(self):
        """
        List all barbers
        """
        barbers = get_all_barbers()
        return [barber.to_dict() for barber in barbers], 200

    @barber_ns.expect(barber_model)
    @barber_ns.doc('create_barber')
    def post(self):
        """
        Create a new barber
        """
        data = request.get_json()
        name = data.get('name')
        barbershop_id = data.get('barbershop_id')
        photo_url = data.get('photo_url')
        new_barber = create_barber(name, barbershop_id, photo_url)
        return new_barber.to_dict(), 201


@barber_ns.route('/<int:barber_id>')
class Barber(Resource):
    @barber_ns.doc('get_barber_by_id')
    def get(self, barber_id):
        """
        Get a barber by ID
        """
        barber = get_barber_by_id(barber_id)
        if barber:
            return barber.to_dict(), 200
        return {'error': 'Barber not found'}, 404

    @barber_ns.expect(barber_model)
    @barber_ns.doc('update_barber')
    def patch(self, barber_id):
        """
        Update a barber by ID
        """
        data = request.get_json()
        updated_barber = update_barber(barber_id, data)
        if updated_barber:
            return updated_barber.to_dict(), 200
        return {'error': 'Barber not found'}, 404

    @barber_ns.doc('delete_barber')
    def delete(self, barber_id):
        """
        Delete a barber by ID
        """
        deleted = delete_barber(barber_id)
        if deleted:
            return {'message': 'Barber deleted successfully'}, 200
        return {'error': 'Barber not found'}, 404


@barber_ns.route('/<int:barber_id>/availability')
class BarberAvailability(Resource):
    @barber_ns.expect(availability_model)
    @barber_ns.doc('update_barber_availability')
    def patch(self, barber_id):
        """
        Update barber availability by ID
        """
        data = request.get_json()
        available = data.get('available')
        updated_barber = update_barber_availability(barber_id, available)
        if updated_barber:
            return updated_barber.to_dict(), 200
        return {'error': 'Barber not found'}, 404

@barber_ns.route('/barbershop/<int:barbershop_id>')
class GetBarbersByBarbershop(Resource):
    @barber_ns.doc('get_barbers_by_barbershop')
    def get(self, barbershop_id):
        """
        Get all barbers working in a specific barbershop
        """
        barbers = get_barbers_by_barbershop(barbershop_id)
        return [barber.to_dict() for barber in barbers], 200 if barbers else {'error': 'No barbers found'}, 404

@barber_ns.route('/availability/<string:status>')
class GetBarbersByAvailability(Resource):
    @barber_ns.doc('get_barbers_by_availability')
    def get(self, status):
        """
        Get barbers by availability status
        """
        available = True if status.lower() == 'available' else False
        barbers = get_barbers_by_availability(available)
        return [barber.to_dict() for barber in barbers], 200 if barbers else {'error': 'No barbers found with specified availability'}, 404

@barber_ns.route('/<int:barber_id>/reviews')
class GetBarberReviews(Resource):
    @barber_ns.doc('get_barber_reviews')
    def get(self, barber_id):
        """
        Get all reviews of a barber
        """
        reviews = get_reviews_for_barber(barber_id)
        return [review.to_dict() for review in reviews], 200 if reviews else {'error': 'No reviews found'}, 404

@barber_ns.route('/search/<string:name>')
class SearchBarbersByName(Resource):
    @barber_ns.doc('search_barbers_by_name')
    def get(self, name):
        """
        Search for barbers by name
        """
        barbers = search_barbers_by_name(name)
        return [barber.to_dict() for barber in barbers], 200 if barbers else {'error': 'No barbers found'}, 404