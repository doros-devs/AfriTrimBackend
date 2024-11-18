from flask_restx import Namespace, Resource, fields
from flask import request
from services.barbershop_service import create_barbershop, add_barber_to_barbershop, add_service_to_barbershop, schedule_barber, create_review, check_payment_status

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
