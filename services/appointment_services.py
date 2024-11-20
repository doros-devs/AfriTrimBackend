from app import db
from models import Appointment
from datetime import datetime

# Service to retrieve all appointments
def get_all_appointments():
    return Appointment.query.all()


# Service to create an appointment with validation for overlapping appointments
def create_appointment(data):
    appointment_time = datetime.strptime(data.get('appointment_time'), "%Y-%m-%dT%H:%M:%S.%f")

    # Prevent overlapping appointments
    overlapping_appointments = Appointment.query.filter(
        Appointment.barber_id == data.get('barber_id'),
        Appointment.appointment_time == appointment_time
    ).first()

    if overlapping_appointments:
        raise ValueError("The barber is already booked at this time.")

    appointment = Appointment(
        client_id=data.get('client_id'),
        barber_id=data.get('barber_id'),
        service_id=data.get('service_id'),
        appointment_time=appointment_time,
        duration=data.get('duration', 30),  # Default duration of 30 mins
        created_at=datetime.now()
    )
    db.session.add(appointment)
    db.session.commit()
    return appointment


# Service to update appointment status
def update_appointment_status(appointment_id, status):
    appointment = get_appointment_by_id(appointment_id)
    if appointment:
        appointment.status = status
        appointment.updated_at = datetime.now()
        db.session.commit()
    return appointment


# Service to retrieve all upcoming appointments for a barber
def get_upcoming_appointments_for_barber(barber_id):
    now = datetime.now()
    return Appointment.query.filter(
        Appointment.barber_id == barber_id,
        Appointment.appointment_time > now
    ).all()

# Service to get appointment by ID
def get_appointment_by_id(appointment_id):
    return Appointment.query.get_or_404(appointment_id)

# Service to update an appointment
def update_appointment(appointment_id, data):
    appointment = get_appointment_by_id(appointment_id)
    if 'client_name' in data:
        appointment.client_name = data['client_name']
    if 'barber_id' in data:
        appointment.barber_id = data['barber_id']
    if 'service_id' in data:
        appointment.service_id = data['service_id']
    if 'appointment_time' in data:
        appointment.appointment_time = datetime.strptime(data['appointment_time'], "%Y-%m-%dT%H:%M:%S")
    db.session.commit()
    return appointment

# Service to delete an appointment
def delete_appointment(appointment_id):
    appointment = get_appointment_by_id(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    return appointment
