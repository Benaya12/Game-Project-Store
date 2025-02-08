from models import db
from models.admin import Admin
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db.init_app(app)

with app.app_context():
    new_admin = Admin(username="ben", password="123")
    db.session.add(new_admin)
    db.session.commit()
    print("Admin user added successfully.")