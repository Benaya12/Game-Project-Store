# create a __init__.py file in the models folder to make all the model act as a package if you dont have it already , also you can make one file with all the models just copy ythe all the code in the files into it
from . import db


# models/loan.py
class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    loan_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    return_date = db.Column(db.DateTime)