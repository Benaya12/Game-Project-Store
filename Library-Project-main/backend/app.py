# routes/loan.py
from flask import Blueprint, request, jsonify
from models.loan import Loan
from models.game import Game
from models.customer import Customer

loan_bp = Blueprint('loan', __name__)

@loan_bp.route('/loans', methods=['POST'])
def create_loan():
    data = request.json
    game_id = data.get('game_id')
    customer_id = data.get('customer_id')

    # Check if the game exists and is available
    game = Game.query.get(game_id)
    if not game or game.quantity <= 0 or game.loan_status:
        return jsonify({"error": "Game not available for loan"}), 400

    # Check if the customer exists
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    # Create the loan
    new_loan = Loan(game_id=game_id, customer_id=customer_id)
    db.session.add(new_loan)

    # Update game status and quantity
    game.loan_status = True
    game.quantity -= 1
    db.session.commit()

    return jsonify({
        "id": new_loan.id,
        "game_id": new_loan.game_id,
        "customer_id": new_loan.customer_id,
        "loan_date": new_loan.loan_date
    }), 201

@loan_bp.route('/loans/<int:id>/return', methods=['POST'])
def return_loan(id):
    loan = Loan.query.get_or_404(id)
    game = Game.query.get(loan.game_id)

    # Update game status and quantity
    game.loan_status = False
    game.quantity += 1

    # Set return date
    loan.return_date = db.func.current_timestamp()
    db.session.commit()

    return jsonify({
        "id": loan.id,
        "game_id": loan.game_id,
        "customer_id": loan.customer_id,
        "return_date": loan.return_date
    }), 200

@loan_bp.route('/loans', methods=['GET'])
def list_loans():
    loans = Loan.query.all()
    loan_list = []
    for loan in loans:
        game = Game.query.get(loan.game_id)
        customer = Customer.query.get(loan.customer_id)
        loan_list.append({
            "id": loan.id,
            "game_title": game.title,
            "customer_name": customer.name,
            "loan_date": loan.loan_date,
            "return_date": loan.return_date
        })
    return jsonify(loan_list), 200