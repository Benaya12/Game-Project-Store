from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from models import db
from models.admin import Admin
from models.game import Game
from models.loan import Loan
from models.customer import Customer

app = Flask(__name__)  # Create a Flask instance
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)  # Initialize the database with the Flask app

# Route to add a new game
@app.route('/games', methods=['POST'])
def add_game():
    data = request.json  # Parse JSON data from the request body
    new_game = Game(
        title=data['title'],
        genre=data['genre'],
        price=data['price'],
        quantity=data['quantity']
    )
    db.session.add(new_game)  # Add the new game to the database session
    db.session.commit()  # Commit the session to save the game in the database
    return jsonify({'message': 'Game added to database.'}), 201

# Route to get all games
@app.route('/games', methods=['GET'])
def get_games():
    try:
        games = Game.query.all()  # Get all games from the database
        games_list = []

        for game in games:  # Loop through each game
            game_data = {
                'id': game.id,
                'title': game.title,
                'genre': game.genre,
                'price': game.price,
                'quantity': game.quantity,
                'loan_status': game.loan_status
            }
            games_list.append(game_data)

        return jsonify({
            'message': 'Games retrieved successfully',
            'games': games_list
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve games',
            'message': str(e)
        }), 500

# Route to delete a game
@app.route('/games/<int:id>', methods=['DELETE'])
def delete_game(id):
    game = Game.query.get_or_404(id)  # Find the game by ID
    db.session.delete(game)  # Delete the game
    db.session.commit()  # Commit the session
    return jsonify({'message': 'Game deleted successfully.'}), 200

# Route to register a new customer
@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully.'}), 201

# Route to get all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    customers_list = []

    for customer in customers:
        customer_data = {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone
        }
        customers_list.append(customer_data)

    return jsonify({
        'message': 'Customers retrieved successfully',
        'customers': customers_list
    }), 200

# Route to loan a game to a customer
@app.route('/loans', methods=['POST'])
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
        "message": "Game loaned successfully",
        "loan_id": new_loan.id,
        "game_id": new_loan.game_id,
        "customer_id": new_loan.customer_id,
        "loan_date": new_loan.loan_date
    }), 201

# Route to return a loaned game
@app.route('/loans/<int:id>/return', methods=['POST'])
def return_loan(id):
    loan = Loan.query.get_or_404(id)
    game = Game.query.get(loan.game_id)

    # Update game status and quantity
    game.loan_status = False
    game.quantity += 1

    # Set return date
    loan.return_date = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "message": "Game returned successfully",
        "loan_id": loan.id,
        "game_id": loan.game_id,
        "customer_id": loan.customer_id,
        "return_date": loan.return_date
    }), 200

# Route to get all loans
@app.route('/loans', methods=['GET'])
def get_loans():
    loans = Loan.query.all()
    loans_list = []

    for loan in loans:
        game = Game.query.get(loan.game_id)
        customer = Customer.query.get(loan.customer_id)
        loans_list.append({
            "id": loan.id,
            "game_title": game.title,
            "customer_name": customer.name,
            "loan_date": loan.loan_date,
            "return_date": loan.return_date
        })

    return jsonify({
        "message": "Loans retrieved successfully",
        "loans": loans_list
    }), 200

# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all database tables defined in your models
    app.run(debug=True)  # Start the Flask application in debug mode