from app import db
from models import Sale
from datetime import datetime

def get_all_sales():
    return Sale.query.all()

def create_sale(data):
    sale = Sale(
        customer_name=data.get('customer_name'),
        barbershop_id=data.get('barbershop_id'),
        barber_id=data.get('barber_id'),
        invoice_id=data.get('invoice_id'),
        sale_date=datetime.now()
    )
    db.session.add(sale)
    db.session.commit()
    return sale

def update_sale(sale_id, data):
    sale = Sale.query.get(sale_id)
    if sale:
        if 'customer_name' in data:
            sale.customer_name = data['customer_name']
        if 'barbershop_id' in data:
            sale.barbershop_id = data['barbershop_id']
        if 'barber_id' in data:
            sale.barber_id = data['barber_id']
        if 'invoice_id' in data:
            sale.invoice_id = data['invoice_id']
        db.session.commit()
    return sale

def delete_sale(sale_id):
    sale = Sale.query.get(sale_id)
    if sale:
        db.session.delete(sale)
        db.session.commit()
    return sale
