from app import db, create_app

# Create an app instance
app = create_app()

# Use the application context to interact with the database
with app.app_context():
    # Drop all tables
    db.drop_all()

    # Create all tables
    db.create_all()

    print("Database has been reset successfully!")
