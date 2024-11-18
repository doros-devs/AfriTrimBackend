from models import Barbershop, Review, Appointment, Service
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

def create_appointment(client_name, barber_id, service_id, appointment_time):
    appointment = Appointment(
        client_name=client_name,
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
