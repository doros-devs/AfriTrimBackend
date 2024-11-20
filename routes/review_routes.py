from flask import request
from flask_restx import Namespace, Resource, fields
from services.review_service import get_reviews, create_review, update_review, delete_review, get_reviews_by_barber_id, \
    get_average_rating_for_barber, can_user_leave_review

# Define Namespace
review_ns = Namespace('reviews', description='Operations related to reviews')

# Define Swagger models for request validation
review_model = review_ns.model('Review', {
    'rating': fields.Integer(required=True, description='Review rating'),
    'comment': fields.String(description='Review comment'),
    'barber_id': fields.Integer(required=True, description='Barber ID')
})

update_review_model = review_ns.model('UpdateReview', {
    'rating': fields.Integer(description='Review rating'),
    'comment': fields.String(description='Review comment')
})


# Routes
@review_ns.route('/')
class ReviewList(Resource):
    @review_ns.doc('get_reviews')
    def get(self):
        """
        Get all reviews
        """
        reviews = get_reviews()
        return [review.to_dict() for review in reviews], 200

    @review_ns.expect(review_model)
    @review_ns.doc('create_review')
    def post(self):
        """
        Create a new review
        """
        data = request.get_json()
        rating = data.get('rating')
        comment = data.get('comment')
        barber_id = data.get('barber_id')

        if rating is None or barber_id is None:
            return {'error': 'Rating and barber_id are required fields'}, 400

        review = create_review(rating, comment, barber_id)
        return review.to_dict(), 201


@review_ns.route('/<int:review_id>')
class Review(Resource):
    @review_ns.expect(update_review_model)
    @review_ns.doc('update_review')
    def patch(self, review_id):
        """
        Update a review by ID
        """
        data = request.get_json()
        rating = data.get('rating')
        comment = data.get('comment')

        review = update_review(review_id, rating, comment)
        if review:
            return review.to_dict(), 200
        return {'error': 'Review not found'}, 404

    @review_ns.doc('delete_review')
    def delete(self, review_id):
        """
        Delete a review by ID
        """
        success = delete_review(review_id)
        if success:
            return {'message': 'Review deleted successfully'}, 200
        return {'error': 'Review not found'}, 404

@review_ns.route('/barber/<int:barber_id>')
class BarberReviews(Resource):
    @review_ns.doc('get_reviews_by_barber_id')
    def get(self, barber_id):
        """
        Get all reviews for a specific barber
        """
        reviews = get_reviews_by_barber_id(barber_id)
        if reviews:
            return [review.to_dict() for review in reviews], 200
        return {'error': 'No reviews found for this barber'}, 404

@review_ns.route('/barber/<int:barber_id>/average-rating')
class BarberAverageRating(Resource):
    @review_ns.doc('get_average_rating_for_barber')
    def get(self, barber_id):
        """
        Get average rating for a specific barber
        """
        average_rating = get_average_rating_for_barber(barber_id)
        return {'barber_id': barber_id, 'average_rating': average_rating}, 200

@review_ns.route('/barber/<int:barber_id>/can-review')
class CanReview(Resource):
    @review_ns.doc('can_user_leave_review')
    def get(self, barber_id):
        """
        Check if user can leave a review for a specific barber
        """
        user_id = request.args.get('user_id')  # Assume user_id is provided as a query parameter
        if not user_id:
            return {'error': 'User ID is required'}, 400

        if can_user_leave_review(user_id, barber_id):
            return {'can_review': True}, 200
        return {'can_review': False}, 403
