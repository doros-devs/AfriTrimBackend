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
