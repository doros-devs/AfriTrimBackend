from app import db
from models import Appointment
from datetime import datetime

# Service to retrieve all appointments
def get_all_appointments():
    return Appointment.query.all()

# Service to create an appointment
def create_appointment(data):
    appointment = Appointment(
        client_name=data.get('client_name'),
        barber_id=data.get('barber_id'),
        service_id=data.get('service_id'),
        appointment_time=datetime.strptime(data.get('appointment_time'), "%Y-%m-%dT%H:%M:%S"),
        created_at=datetime.now()
    )
    db.session.add(appointment)
    db.session.commit()
    return appointment

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
