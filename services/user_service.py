from models import Client, Barber, Admin
from app import db
from sqlalchemy.exc import SQLAlchemyError
from firebase_admin import auth

# User Services


def create_user(data, role):
    """
    Create a user in the database based on role (Admin, Barber, Client).
    """
    try:
        if role == "admin":
            user = Admin(name=data["name"], email=data["email"], uid=data["uid"])
            custom_claims = {"admin": True, "barber": False, "client": False}
        elif role == "barber":
            user = Barber(name=data["name"], email=data["email"], uid=data["uid"], barbershop_id=data.get("barbershop_id"))
            custom_claims = {"admin": False, "barber": True, "client": False}
        elif role == "client":
            user = Client(name=data["name"], email=data["email"], uid=data["uid"])
            custom_claims = {"admin": False, "barber": False, "client": True}
        else:
            raise ValueError("Invalid role provided")

        db.session.add(user)
        db.session.commit()

        # Set custom claims for the user in Firebase
        auth.set_custom_user_claims(data["uid"], custom_claims)

        return user
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Failed to create user due to database error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to set custom claims: {str(e)}")


def get_user_by_uid(uid):
    """
    Fetch a user by their Firebase UID.
    """
    try:
        admin = Admin.query.filter_by(uid=uid).first()
        if admin:
            return admin, "admin"

        barber = Barber.query.filter_by(uid=uid).first()
        if barber:
            return barber, "barber"

        client = Client.query.filter_by(uid=uid).first()
        if client:
            return client, "client"

        return None, None
    except SQLAlchemyError as e:
        raise ValueError(f"Failed to fetch user: {str(e)}")


def update_user_role(uid, new_role):
    """
    Update user role.
    """
    user, current_role = get_user_by_uid(uid)
    if not user:
        raise ValueError("User not found")
    try:
        if current_role == "client" and new_role == "barber":
            # Move from client to barber, potentially add barbershop association
            user = Barber(name=user.name, email=user.email, uid=user.uid, barbershop_id=user.barbershop_id)
        elif current_role == "barber" and new_role == "admin":
            # Move from barber to admin
            user = Admin(name=user.name, email=user.email, uid=user.uid)
        else:
            raise ValueError("Invalid role change requested")

        db.session.add(user)
        db.session.commit()
        return user
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Failed to update user role: {str(e)}")


def delete_user(uid):
    user, _ = get_user_by_uid(uid)
    if not user:
        raise ValueError("User not found")
    try:
        # Delete the user from the backend database
        db.session.delete(user)
        db.session.commit()

        # Delete the user from Firebase using Firebase Admin SDK
        auth.delete_user(uid)
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Failed to delete user from backend: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to delete user from Firebase: {str(e)}")

# Add missing service functions
def update_user(uid, data):
    """
    Update user details by Firebase UID.
    """
    user, _ = get_user_by_uid(uid)
    if not user:
        raise ValueError("User not found")
    try:
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return user
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Failed to update user: {str(e)}")