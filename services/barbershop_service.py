from models import Barbershop, Barber, Service, Review, Payment
from app import db

# Updated function to use admin_id instead of owner_id
def create_barbershop(admin_id, name, location):  # Changed owner_id to admin_id
    barbershop = Barbershop(admin_id=admin_id, name=name, location=location)  # Changed owner_id to admin_id
    db.session.add(barbershop)
    db.session.commit()
    return barbershop

# Function to add a barber to a barbershop
def add_barber_to_barbershop(barbershop_id, name):
    barber = Barber(name=name, barbershop_id=barbershop_id)
    db.session.add(barber)
    db.session.commit()
    return barber

# Function to add a service to a barbershop
def add_service_to_barbershop(barbershop_id, name, price):
    service = Service(name=name, price=price, barbershop_id=barbershop_id)
    db.session.add(service)
    db.session.commit()
    return service

# Function to schedule the availability of a barber
def schedule_barber(barber_id, available):
    barber = Barber.query.get(barber_id)
    if barber:
        barber.available = available
        db.session.commit()
    return barber

# Function to create a review for a barber
def create_review(barber_id, rating, comment):
    review = Review(barber_id=barber_id, rating=rating, comment=comment)
    db.session.add(review)
    db.session.commit()
    return review

# Updated function to use admin_id instead of owner_id
def check_payment_status(admin_id):  # Changed owner_id to admin_id
    payment = Payment.query.filter_by(admin_id=admin_id).order_by(Payment.paid_at.desc()).first()  # Changed owner_id to admin_id
    if payment:
        return payment.status
    return 'No Payment Found'
