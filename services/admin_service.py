from models import Barbershop, Payment, Barber, Service, Appointment, Sale, Review, Invoice, Client, Admin
from app import db
from datetime import datetime

# Utility function for updating entity attributes
def create_admin(data):
    admin = Admin(
        uid=data.get('uid'),
        name=data.get('name'),
        email=data.get('email'),
        is_active=True,
        created_at=datetime.now()
    )
    db.session.add(admin)
    db.session.commit()
    return admin

def suspend_admin(admin_id):
    admin = Admin.query.get(admin_id)
    if admin:
        admin.is_active = False
        db.session.commit()
        return admin
    return None

def delete_admin(admin_id):
    admin = Admin.query.get(admin_id)
    if admin:
        db.session.delete(admin)
        db.session.commit()
        return True
    return False

def get_admin_by_id(admin_id):
    return Admin.query.get(admin_id)


def update_entity(entity, data):
    for key, value in data.items():
        if hasattr(entity, key):
            setattr(entity, key, value)
    db.session.commit()
    return entity

# Admin Services
def get_all_barbershops():
    return Barbershop.query.all()


def update_payment_status(admin_id, status):  # Replaced owner_id with admin_id
    payment = Payment.query.filter_by(admin_id=admin_id).order_by(Payment.paid_at.desc()).first()  # Replaced owner_id with admin_id
    if not payment:
        raise ValueError(f"Payment for admin_id {admin_id} not found")  # Updated error message
    payment.status = status
    db.session.commit()
    return payment


def manage_barbershop(barbershop_id, data):
    barbershop = Barbershop.query.get(barbershop_id)
    if not barbershop:
        raise ValueError(f"Barbershop with id {barbershop_id} not found")
    return update_entity(barbershop, data)


def manage_barber(barber_id, data):
    barber = Barber.query.get(barber_id)
    if not barber:
        raise ValueError(f"Barber with id {barber_id} not found")
    return update_entity(barber, data)


def manage_service(service_id, data):
    service = Service.query.get(service_id)
    if not service:
        raise ValueError(f"Service with id {service_id} not found")
    return update_entity(service, data)


def manage_appointment(appointment_id, data):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        raise ValueError(f"Appointment with id {appointment_id} not found")
    if 'appointment_time' in data:
        data['appointment_time'] = datetime.strptime(data['appointment_time'], "%Y-%m-%d %H:%M:%S")
    return update_entity(appointment, data)


def manage_invoice(invoice_id, data):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        raise ValueError(f"Invoice with id {invoice_id} not found")
    if 'paid_at' in data:
        data['paid_at'] = datetime.strptime(data['paid_at'], "%Y-%m-%d %H:%M:%S")
    return update_entity(invoice, data)


def manage_sale(sale_id, data):
    sale = Sale.query.get(sale_id)
    if not sale:
        raise ValueError(f"Sale with id {sale_id} not found")
    return update_entity(sale, data)


def manage_client_review(review_id, data):
    review = Review.query.get(review_id)
    if not review:
        raise ValueError(f"Review with id {review_id} not found")
    return update_entity(review, data)


def manage_client(client_id, data):
    client = Client.query.get(client_id)
    if not client:
        raise ValueError(f"Client with id {client_id} not found")
    return update_entity(client, data)
