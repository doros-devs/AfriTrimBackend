from sqlalchemy import func

from models import Review
from app import db

# Get all reviews
def get_reviews():
    return Review.query.all()

# Create a review
def create_review(rating, comment, barber_id):
    review = Review(rating=rating, comment=comment, barber_id=barber_id)
    db.session.add(review)
    db.session.commit()
    return review

# Update a review
def update_review(review_id, rating=None, comment=None):
    review = Review.query.get(review_id)
    if review:
        if rating is not None:
            review.rating = rating
        if comment is not None:
            review.comment = comment
        db.session.commit()
    return review

# Delete a review
def delete_review(review_id):
    review = Review.query.get(review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
        return True
    return False

def get_reviews_by_barber_id(barber_id):
    return Review.query.filter_by(barber_id=barber_id).all()

def get_average_rating_for_barber(barber_id):
    average = db.session.query(func.avg(Review.rating)).filter_by(barber_id=barber_id).scalar()
    return average if average else 0

def can_user_leave_review(user_id, barber_id):
    # Placeholder logic, you may need to check appointment history, etc.
    return True
