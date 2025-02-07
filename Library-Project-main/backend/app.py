from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db
from models.admin import Admin
from models.game import Game
from models.loan import Loan
from models.customer import Customer

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Query the Admin table for the provided username
    admin = Admin.query.filter_by(username=username).first()

    if admin and admin.password == password:  # Check if the admin exists and the password matches
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

# Add admin route
@app.route('/add-admin', methods=['POST'])
def add_admin():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if the admin already exists
    existing_admin = Admin.query.filter_by(username=username).first()
    if existing_admin:
        return jsonify({'error': 'Admin already exists'}), 400

    # Create a new admin
    new_admin = Admin(username=username, password=password)
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({'message': 'Admin added successfully'}), 201

# Add game route
@app.route('/games', methods=['POST'])
def add_game():
    data = request.json
    try:
        new_game = Game(
            title=data['title'],
            genre=data['genre'],
            price=data['price'],
            quantity=data['quantity']
        )
        db.session.add(new_game)
        db.session.commit()
        return jsonify({'message': 'Game added to database.'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to add game', 'message': str(e)}), 500

# Route to get all games
@app.route('/games', methods=['GET'])
def get_games():
    try:
        games = Game.query.all()
        games_list = []

        for game in games:
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
    game = Game.query.get_or_404(id)
    db.session.delete(game)
    db.session.commit()
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

# Route to delete a customer
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully.'}), 200

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
    loan.return_date = db.func.current_timestamp()
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
        db.create_all()  # Create all database tables
    app.run(debug=True)
