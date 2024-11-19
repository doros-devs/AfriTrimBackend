from datetime import datetime
from app import db

class Barbershop(db.Model):
    __tablename__ = 'barbershops'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    admin_id = db.Column(db.String, nullable=False)  # Replaced owner_id with admin_id to reference the admin
    location = db.Column(db.String, nullable=True)
    services = db.relationship('Service', backref=db.backref('barbershop', lazy=True), cascade="all, delete-orphan")
    barbers = db.relationship('Barber', backref=db.backref('barbershop', lazy=True), cascade="all, delete-orphan")
    photo_url = db.Column(db.String, nullable=True)  # URL of the barbershop image
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "admin_id": self.admin_id,  # Replaced owner_id with admin_id
            "location": self.location,
            "photo_url": self.photo_url,
            "services": [service.to_dict() for service in self.services],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Barber(db.Model):
    __tablename__ = 'barbers'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, nullable=False, unique=True)  # Firebase UID
    name = db.Column(db.String, nullable=False)
    barbershop_id = db.Column(db.Integer, db.ForeignKey('barbershops.id'))
    available = db.Column(db.Boolean, default=True)
    photo_url = db.Column(db.String, nullable=True)  # URL of the barber's profile picture
    reviews = db.relationship('Review', backref=db.backref('barber', lazy=True), cascade="all, delete-orphan")
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
    photo_url = db.Column(db.String, nullable=True)  # URL of the service image
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
    admin_id = db.Column(db.String, nullable=False)  # Replaced owner_id with admin_id to reference the admin
    amount = db.Column(db.Integer, nullable=False)
    paid_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    status = db.Column(db.String, default='Pending')

    def to_dict(self):
        return {
            "id": self.id,
            "admin_id": self.admin_id,  # Replaced owner_id with admin_id
            "amount": self.amount,
            "paid_at": self.paid_at.isoformat(),
            "status": self.status,
            "updated_at": self.updated_at.isoformat()
        }


class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Client', backref=db.backref('sales', lazy=True), cascade="all, delete-orphan")
    barbershop_id = db.Column(db.Integer, db.ForeignKey('barbershops.id'), nullable=False)
    barbershop = db.relationship('Barbershop', backref=db.backref('sales', lazy=True), cascade="all, delete-orphan")
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=True)
    sale_date = db.Column(db.DateTime, default=datetime.now)
    invoice = db.relationship('Invoice', backref=db.backref('sales', lazy=True), cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'client_name': self.client.name,
            'barbershop_id': self.barbershop_id,
            'barbershop_name': self.barbershop.name,
            'invoice_id': self.invoice_id,
            'sale_date': self.sale_date.isoformat()
        }


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Client', backref=db.backref('appointments', lazy=True), cascade="all, delete-orphan")
    barber_id = db.Column(db.Integer, db.ForeignKey('barbers.id'), nullable=False)
    barber = db.relationship('Barber', backref=db.backref('appointments', lazy=True), cascade="all, delete-orphan")
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    service = db.relationship('Service', backref=db.backref('appointments', lazy=True), cascade="all, delete-orphan")
    appointment_time = db.Column(db.DateTime, nullable=False)
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
            'created_at': self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Client', backref=db.backref('invoices', lazy=True), cascade="all, delete-orphan")
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
            'paid_at': self.paid
        }

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, nullable=False, unique=True)  # Firebase UID
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=True)
    photo_url = db.Column(db.String, nullable=True)  # URL of the client's profile picture
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

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, nullable=False, unique=True)  # Firebase UID
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }