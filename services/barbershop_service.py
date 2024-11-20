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

# Service to retrieve all barbershops
def get_all_barbershops():
    """
    Retrieve all barbershops from the database
    """
    return Barbershop.query.all()

# Service to retrieve a barbershop by ID
def get_barbershop_by_id(barbershop_id):
    """
    Retrieve a specific barbershop by its ID
    """
    return Barbershop.query.get_or_404(barbershop_id)

# Service to retrieve all barbers associated with a barbershop
def get_barbers_by_barbershop(barbershop_id):
    """
    Retrieve all barbers associated with a specific barbershop
    """
    barbershop = get_barbershop_by_id(barbershop_id)
    return barbershop.barbers

# Service to retrieve all services provided by a barbershop
def get_services_by_barbershop(barbershop_id):
    """
    Retrieve all services provided by a specific barbershop
    """
    barbershop = get_barbershop_by_id(barbershop_id)
    return barbershop.services

# Search barbershops by name or location
def search_barbershops(query):
    return Barbershop.query.filter(
        (Barbershop.name.ilike(f'%{query}%')) | (Barbershop.location.ilike(f'%{query}%'))
    ).all()

# Update barbershop details
def update_barbershop(barbershop_id, data):
    barbershop = Barbershop.query.get(barbershop_id)
    if barbershop:
        if 'name' in data:
            barbershop.name = data['name']
        if 'location' in data:
            barbershop.location = data['location']
        if 'photo_url' in data:
            barbershop.photo_url = data['photo_url']
        db.session.commit()
    return barbershop

# Delete a barbershop
def delete_barbershop(barbershop_id):
    barbershop = Barbershop.query.get(barbershop_id)
    if barbershop:
        db.session.delete(barbershop)
        db.session.commit()
        return True
    return False

# List all barbers for a barbershop
def list_barbers_for_barbershop(barbershop_id):
    barbershop = Barbershop.query.get(barbershop_id)
    if barbershop:
        return barbershop.barbers
    return []

# List all services for a barbershop
def list_services_for_barbershop(barbershop_id):
    barbershop = Barbershop.query.get(barbershop_id)
    if barbershop:
        return barbershop.services
    return []
