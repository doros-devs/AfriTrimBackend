from app import db
from models import Admin, Client, Barber, Barbershop, Service, Review, Payment, Sale, Appointment, Invoice
from datetime import datetime
from app import db, create_app  # Import your Flask app factory function
from faker import Faker
import random

# Initialize Faker for generating random data
fake = Faker()

# Create an app instance
app = create_app()

# Use the application context
with app.app_context():
    # Drop all tables
    db.drop_all()

    # Create all tables
    db.create_all()

    # 1. Create Admins
    admins = [
        Admin(uid=fake.uuid4(), name=fake.name(), email=f"admin{i}@afritrim.com") for i in range(3)
    ]
    db.session.add_all(admins)
    db.session.commit()

    # 2. Create Clients
    clients = [
        Client(uid=fake.uuid4(), name=fake.name(), email=fake.email(), phone_number=fake.phone_number()) for _ in range(10)
    ]
    db.session.add_all(clients)
    db.session.commit()

    # 3. Create Barbershops and Barbers
    barbershops = []
    barbers = []
    for i in range(5):
        barbershop = Barbershop(
            name=fake.company(),
            location=fake.address(),
            admin_id=random.choice(admins).id,  # Assign barbershop to a random admin
            photo_url=fake.image_url()
        )
        db.session.add(barbershop)
        db.session.commit()  # Commit here to get the barbershop ID
        barbershops.append(barbershop)

        # Create barbers for each barbershop
        for _ in range(2):
            barber = Barber(
                uid=fake.uuid4(),
                name=fake.name(),
                barbershop_id=barbershop.id,
                available=random.choice([True, False]),
                photo_url=fake.image_url()
            )
            barbers.append(barber)

    db.session.add_all(barbers)
    db.session.commit()

    # 4. Create Services for each Barbershop
    services = []
    for barbershop in barbershops:
        for _ in range(4):
            service = Service(
                name=fake.bs(),
                price=random.randint(10, 100),
                barbershop_id=barbershop.id,
                photo_url=fake.image_url()
            )
            services.append(service)

    db.session.add_all(services)
    db.session.commit()

    # 5. Create Reviews for Barbers
    reviews = []
    for barber in barbers:
        for _ in range(2):
            review = Review(
                rating=random.randint(1, 5),
                comment=fake.text(),
                barber_id=barber.id,
                created_at=fake.date_time_this_year(),
                updated_at=fake.date_time_this_year()
            )
            reviews.append(review)

    db.session.add_all(reviews)
    db.session.commit()

    # 6. Create Payments
    payments = []
    for _ in range(15):
        payment = Payment(
            admin_id=random.choice(admins).id,  # Assign payment to a random admin
            amount=random.randint(50, 200),
            paid_at=fake.date_time_this_year(),
            status=random.choice(['Pending', 'Completed', 'Failed'])
        )
        payments.append(payment)

    db.session.add_all(payments)
    db.session.commit()

    # 7. Create Sales
    sales = []
    for _ in range(10):
        sale = Sale(
            client_id=random.choice(clients).id,
            barbershop_id=random.choice(barbershops).id,
            invoice_id=None,  # Will be updated later when creating invoices
            sale_date=fake.date_time_this_year()
        )
        sales.append(sale)

    db.session.add_all(sales)
    db.session.commit()

    # 8. Create Appointments
    appointments = []
    for _ in range(15):
        appointment = Appointment(
            client_id=random.choice(clients).id,
            barber_id=random.choice(barbers).id,
            service_id=random.choice(services).id,
            appointment_time=fake.future_datetime(end_date="+30d"),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        appointments.append(appointment)

    db.session.add_all(appointments)
    db.session.commit()

    # 9. Create Invoices
    invoices = []
    for sale in sales:
        invoice = Invoice(
            client_id=sale.client_id,
            barbershop_id=sale.barbershop_id,
            amount=random.uniform(50, 300),
            status=random.choice(['Pending', 'Paid']),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year()
        )
        invoices.append(invoice)
        sale.invoice_id = invoice.id  # Update sale with corresponding invoice

    db.session.add_all(invoices)
    db.session.commit()

    print("Database seeded successfully!")
