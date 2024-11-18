from app import db
from models import Invoice
from datetime import datetime

# Function to create a new invoice
def create_invoice(data):
    invoice = Invoice(
        customer_name=data.get('customer_name'),
        barbershop_id=data.get('barbershop_id'),
        amount=data.get('amount'),
        status=data.get('status', 'Pending'),
        created_at=datetime.now()
    )
    db.session.add(invoice)
    db.session.commit()
    return invoice

# Function to get an invoice by ID
def get_invoice_by_id(invoice_id):
    return Invoice.query.get(invoice_id)

# Function to get all invoices
def get_all_invoices():
    return Invoice.query.all()

# Function to update invoice status
def update_invoice_status(invoice_id, status):
    invoice = get_invoice_by_id(invoice_id)
    if invoice:
        invoice.status = status
        if status.lower() == 'paid':
            invoice.paid_at = datetime.now()
        db.session.commit()
        return invoice
    return None
