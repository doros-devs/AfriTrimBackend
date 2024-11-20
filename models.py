from datetime import datetime
from app import db

class Barbershop(db.Model):
    __tablename__ = 'barbershops'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    admin_id = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=True)
    services = db.relationship('Service', backref='barbershop', lazy=True, cascade="all, delete-orphan")
    barbers = db.relationship('Barber', backref='barbershop', lazy=True, cascade="all, delete-orphan")
    photo_url = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "admin_id": self.admin_id,
            "location": self.location,
            "photo_url": self.photo_url,
            "services": [service.to_dict() for service in self.services],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Barber(db.Model):
    __tablename__ = 'barbers'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    barbershop_id = db.Column(db.Integer, db.ForeignKey('barbershops.id'))
    available = db.Column(db.Boolean, default=True)
    photo_url = db.Column(db.String, nullable=True)
    reviews = db.relationship('Review', backref='barber', lazy=True)
    appointments = db.relationship('Appointment', backref='barber_appointments', lazy=True)  # Updated backref

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "barbershop_id": self.barbershop_id,
            "available": self.available,
            "photo_url": self.photo_url,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "reviews": [review.to_dict() for review in self.reviews]
        }


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    barbershop_id = db.Column(db.Integer, db.ForeignKey('barbershops.id'))
    photo_url = db.Column(db.String, nullable=True)
    appointments = db.relationship('Appointment', backref='service_appointments', lazy=True)  # Updated backref
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "photo_url": self.photo_url,
            "barbershop_id": self.barbershop_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Client', backref='client_appointments', lazy=True)  # Updated backref
    barber_id = db.Column(db.Integer, db.ForeignKey('barbers.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String, default='Scheduled')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'client_name': self.client.name,
            'barber_id': self.barber_id,
            'service_id': self.service_id,
            'appointment_time': self.appointment_time.isoformat(),
            'duration': self.duration,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String, nullable=True)
    barber_id = db.Column(db.Integer, db.ForeignKey('barbers.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "comment": self.comment,
            "barber_id": self.barber_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=True)
    paid_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    status = db.Column(db.String, default='Pending')

    def to_dict(self):
        return {
            "id": self.id,
            "admin_id": self.admin_id,
            "amount": self.amount,
            "sale_id": self.sale_id,
            "invoice_id": self.invoice_id,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "status": self.status,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    barbershop_id = db.Column(db.Integer, db.ForeignKey('barbershops.id'), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    expense = db.Column(db.Float, nullable=False)
    profit = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, client_id, barbershop_id, invoice_id, amount, expense):
        self.client_id = client_id
        self.barbershop_id = barbershop_id
        self.invoice_id = invoice_id
        self.amount = amount
        self.expense = expense
        self.profit = amount - expense

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'barbershop_id': self.barbershop_id,
            'invoice_id': self.invoice_id,
            'amount': self.amount,
            'expense': self.expense,
            'profit': self.profit,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }



class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True, index=True)
    phone_number = db.Column(db.String(20), nullable=True)
    photo_url = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            "uid": self.uid,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'photo_url': self.photo_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Client', backref='invoices', lazy=True)
    barbershop_id = db.Column(db.Integer, db.ForeignKey('barbershops.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    paid_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'client_name': self.client.name,
            'barbershop_id': self.barbershop_id,
            'amount': self.amount,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'paid_at': self.paid_at
        }


class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    role = db.Column(db.String, default='admin', nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "role": self.role
        }
