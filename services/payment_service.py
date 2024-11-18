from app import db
from models import Payment
from datetime import datetime

def get_all_payments():
    return Payment.query.all()

def create_payment(data):
    payment = Payment(
        admin_id=data.get('admin_id'),
        amount=data.get('amount'),
        paid_at=datetime.now(),
        status=data.get('status', 'Pending')
    )
    db.session.add(payment)
    db.session.commit()
    return payment

# Function to delete a payment by ID
def delete_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if payment:
        db.session.delete(payment)
        db.session.commit()
    return payment

# Function to update/edit a payment by ID
def update_payment(payment_id, data):
    payment = Payment.query.get(payment_id)
    if payment:
        if 'amount' in data:
            payment.amount = data['amount']
        if 'status' in data:
            payment.status = data['status']
        payment.updated_at = datetime.now()
        db.session.commit()
    return payment
