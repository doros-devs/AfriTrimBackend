from models import Service
from app import db

def create_service(name, price, barbershop_id, photo_url=None):
    service = Service(name=name, price=price, barbershop_id=barbershop_id, photo_url=photo_url)
    db.session.add(service)
    db.session.commit()
    return service

def get_all_services():
    return Service.query.all()

def get_service_by_id(service_id):
    return Service.query.get(service_id)

def update_service(service_id, name=None, price=None, photo_url=None):
    service = Service.query.get(service_id)
    if service:
        if name:
            service.name = name
        if price:
            service.price = price
        if photo_url:
            service.photo_url = photo_url
        db.session.commit()
    return service

def delete_service(service_id):
    service = Service.query.get(service_id)
    if service:
        db.session.delete(service)
        db.session.commit()
    return service