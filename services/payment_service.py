from models import Payment, Sale, Invoice
from app import db
from datetime import datetime

def get_all_payments():
    return Payment.query.all()

def create_payment(data):
    invoice_id = data.get('invoice_id')
    sale_id = data.get('sale_id')

    # Validate the invoice ID
    invoice = Invoice.query.get(invoice_id) if invoice_id else None
    if invoice and invoice.status == 'Paid':
        raise ValueError("Invoice is already paid.")

    payment = Payment(
        admin_id=data.get('admin_id'),
        amount=data.get('amount'),
        invoice_id=invoice_id,
        sale_id=sale_id,
        paid_at=datetime.now(),
        status=data.get('status', 'Paid')
    )
    db.session.add(payment)

    # Update invoice status if linked
    if invoice:
        invoice.status = 'Paid'
        invoice.paid_at = datetime.now()

    db.session.commit()
    return payment

def delete_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if payment:
        db.session.delete(payment)
        db.session.commit()
    return payment

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

def get_payments_by_invoice(invoice_id):
    return Payment.query.filter_by(invoice_id=invoice_id).all()

def get_payments_by_sale(sale_id):
    return Payment.query.filter_by(sale_id=sale_id).all()
