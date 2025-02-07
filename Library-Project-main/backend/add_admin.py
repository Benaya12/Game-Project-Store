import sys
from models import db
from models.admin import Admin
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

def create_user(username, password):
    with app.app_context():
        if Admin.query.filter_by(username=username).first():
            print("Error: Username already exists!")
            return

        new_admin = Admin(username=username, password=password)
        db.session.add(new_admin)
        db.session.commit()
        print(f"Admin user '{username}' created successfully!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_user.py USERNAME PASSWORD")
    else:
        create_user(sys.argv[1], sys.argv[2])