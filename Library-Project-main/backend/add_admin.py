from app import app, db
from models.admin import Admin

with app.app_context():
    # Create a new admin
    new_admin = Admin(username='admin', password='password123')
    db.session.add(new_admin)
    db.session.commit()
    print("Admin added successfully!")