from app import db
from models import Sale

# Create a sale
def create_sale(data):
    sale = Sale(
        client_id=data.get('client_id'),
        barbershop_id=data.get('barbershop_id'),
        invoice_id=data.get('invoice_id'),
        amount=data.get('amount'),
        expense=data.get('expense')
    )
    db.session.add(sale)
    db.session.commit()
    return sale

# Update a sale
def update_sale(sale_id, data):
    sale = Sale.query.get(sale_id)
    if sale:
        if 'amount' in data:
            sale.amount = data['amount']
        if 'expense' in data:
            sale.expense = data['expense']
        sale.profit = sale.amount - sale.expense
        db.session.commit()
    return sale

# Delete a sale
def delete_sale(sale_id):
    sale = Sale.query.get(sale_id)
    if sale:
        db.session.delete(sale)
        db.session.commit()
    return sale

# Get total sales, expenses, and profit
def get_total_sales():
    total_sales = db.session.query(db.func.sum(Sale.amount)).scalar() or 0
    total_expenses = db.session.query(db.func.sum(Sale.expense)).scalar() or 0
    total_profit = db.session.query(db.func.sum(Sale.profit)).scalar() or 0
    return {
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'total_profit': total_profit
    }

# Get average sale by barbershop, barber, or service
def get_average_sale(barbershop_id=None, barber_id=None):
    query = Sale.query
    if barbershop_id:
        query = query.filter(Sale.barbershop_id == barbershop_id)
    if barber_id:
        query = query.filter(Sale.barber_id == barber_id)
    avg_sale = db.session.query(db.func.avg(Sale.amount)).scalar() or 0
    return avg_sale

# Service to get all sales
def get_all_sales():
    return Sale.query.all()
