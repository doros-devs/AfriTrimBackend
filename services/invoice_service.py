from app import db
from models import Invoice
from datetime import datetime

# Function to create a new invoice
def create_invoice(data):
    invoice = Invoice(
        client_id=data.get('client_id'),  # Use client_id instead of customer_name
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

# Function to update invoice details
def update_invoice(invoice_id, data):
    invoice = get_invoice_by_id(invoice_id)
    if invoice:
        if 'client_id' in data:
            invoice.client_id = data['client_id']
        if 'barbershop_id' in data:
            invoice.barbershop_id = data['barbershop_id']
        if 'amount' in data:
            invoice.amount = data['amount']
        if 'status' in data:
            invoice.status = data['status']
            if data['status'].lower() == 'paid':
                invoice.paid_at = datetime.now()
        db.session.commit()
        return invoice
    return None

# Function to delete an invoice by ID
def delete_invoice(invoice_id):
    invoice = get_invoice_by_id(invoice_id)
    if invoice:
        db.session.delete(invoice)
        db.session.commit()
        return True
    return False

# Function to get all invoices for a specific client
def get_invoices_for_client(client_id):
    return Invoice.query.filter_by(client_id=client_id).all()

# Function to get all invoices for a specific barbershop
def get_invoices_for_barbershop(barbershop_id):
    return Invoice.query.filter_by(barbershop_id=barbershop_id).all()
