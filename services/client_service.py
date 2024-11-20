from models import Barbershop, Review, Appointment, Service, Client
from app import db
from datetime import datetime

# Client Services
def get_barbershops():
    return Barbershop.query.all()

def get_barbershop_details(barbershop_id):
    return Barbershop.query.get(barbershop_id)

def create_barbershop_review(barbershop_id, rating, comment):
    review = Review(barbershop_id=barbershop_id, rating=rating, comment=comment)
    db.session.add(review)
    db.session.commit()
    return review

def create_barber_review(barber_id, rating, comment):
    review = Review(barber_id=barber_id, rating=rating, comment=comment)
    db.session.add(review)
    db.session.commit()
    return review

def create_appointment(client_id, barber_id, service_id, appointment_time):
    appointment = Appointment(
        client_id=client_id,
        barber_id=barber_id,
        service_id=service_id,
        appointment_time=datetime.strptime(appointment_time, "%Y-%m-%d %H:%M:%S"),
        created_at=datetime.now()
    )
    db.session.add(appointment)
    db.session.commit()
    return appointment


def update_appointment(appointment_id, barber_id=None, service_id=None, appointment_time=None):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        if barber_id is not None:
            appointment.barber_id = barber_id
        if service_id is not None:
            appointment.service_id = service_id
        if appointment_time is not None:
            appointment.appointment_time = datetime.strptime(appointment_time, "%Y-%m-%d %H:%M:%S")
        db.session.commit()
    return appointment

def get_services_by_barbershop(barbershop_id):
    return Service.query.filter_by(barbershop_id=barbershop_id).all()

def create_client(data):
    client = Client(
        uid=data.get('uid'),
        name=data.get('name'),
        email=data.get('email'),
        phone_number=data.get('phone_number'),
        photo_url=data.get('photo_url'),
        created_at=datetime.now()
    )
    db.session.add(client)
    db.session.commit()
    return client

def update_client(client_id, data):
    client = Client.query.get(client_id)
    if client:
        if 'name' in data:
            client.name = data['name']
        if 'email' in data:
            client.email = data['email']
        if 'phone_number' in data:
            client.phone_number = data['phone_number']
        if 'photo_url' in data:
            client.photo_url = data['photo_url']
        client.updated_at = datetime.now()
        db.session.commit()
    return client

def delete_client(client_id):
    client = Client.query.get(client_id)
    if client:
        db.session.delete(client)
        db.session.commit()
        return True
    return False

def get_client_by_id(client_id):
    return Client.query.get(client_id)

