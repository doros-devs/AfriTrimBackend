from models import Barber
from app import db

# Get all barbers
def get_all_barbers():
    return Barber.query.all()

# Get a barber by ID
def get_barber_by_id(barber_id):
    return Barber.query.get(barber_id)

# Create a new barber
def create_barber(name, barbershop_id, photo_url=None):
    new_barber = Barber(name=name, barbershop_id=barbershop_id, photo_url=photo_url)
    db.session.add(new_barber)
    db.session.commit()
    return new_barber

# Update barber details
def update_barber(barber_id, data):
    barber = Barber.query.get(barber_id)
    if barber:
        if 'name' in data:
            barber.name = data['name']
        if 'photo_url' in data:
            barber.photo_url = data['photo_url']
        db.session.commit()
    return barber

# Update barber availability
def update_barber_availability(barber_id, available):
    barber = Barber.query.get(barber_id)
    if barber:
        barber.available = available
        db.session.commit()
    return barber

# Delete a barber
def delete_barber(barber_id):
    barber = Barber.query.get(barber_id)
    if barber:
        db.session.delete(barber)
        db.session.commit()
        return True
    return False

# Get all barbers in a particular barbershop
def get_barbers_by_barbershop(barbershop_id):
    return Barber.query.filter_by(barbershop_id=barbershop_id).all()

# Get all barbers by their availability status
def get_barbers_by_availability(available):
    return Barber.query.filter_by(available=available).all()

# Get all reviews for a specific barber
def get_reviews_for_barber(barber_id):
    barber = Barber.query.get(barber_id)
    return barber.reviews if barber else []

# Search barbers by their name (case insensitive search)
def search_barbers_by_name(name):
    return Barber.query.filter(Barber.name.ilike(f'%{name}%')).all()