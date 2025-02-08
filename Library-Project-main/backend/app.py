from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from datetime import datetime, timedelta
from models import db
from models.game import Game
from models.loan import Loan
from models.admin import Admin
from models.customer import Customer  # Import the Customer model

app = Flask(__name__)  # - create a flask instance
# - enable all routes, allow requests from anywhere (optional - not recommended for security)
CORS(app, resources={r"/*": {"origins": "*"}})

# Specifies the database connection URL. In this case, it's creating a SQLite database
# named 'library.db' in your project directory. The three slashes '///' indicate a
# relative path from the current directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db.init_app(app)  # initializes the database with the flask application

# Helper function to find a customer by email
def find_customer(email):
    customer = Customer.query.filter_by(email=email).first()
    return customer

# this is a decorator from the flask module to define a route for for adding a game, supporting POST requests.(check the decorator summary i sent you and also the exercises)
@app.route('/games', methods=['POST'])
def add_game():
    data = request.json

    # Ensure all required fields are present
    required_fields = ['title', 'genre', 'price', 'quantity']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Create the game object
    new_game = Game(
        title=data['title'],
        genre=data['genre'],
        price=float(data['price']),  # Ensure correct data type
        quantity=int(data['quantity'])  # Ensure correct data type
    )
    
    db.session.add(new_game)
    db.session.commit()

    return jsonify({'message': 'Game added successfully!', 'game': {
        'id': new_game.id,
        'title': new_game.title,
        'genre': new_game.genre,
        'price': new_game.price,
        'quantity': new_game.quantity
    }}), 201

# a decorator to Define a new route that handles GET requests
@app.route('/games', methods=['GET'])
def get_games():
    try:
        games = Game.query.all()  # Get all the games from the database

        # Create empty list to store formatted game data we get from the database
        games_list = []

        for game in games:  # Loop through each game from database
            game_data = {
                'id': game.id,
                'title': game.title,
                'genre': game.genre,  # Use the correct field 'genre'
                'price': game.price,
                'quantity': game.quantity,
                'loan_status': game.loan_status
            }
            games_list.append(game_data)  # Add the iterated game dictionary to our list

        return jsonify({
            'message': 'games retrieved successfully',
            'games': games_list  # Return the list of games
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve games',
            'message': str(e)
        }), 500

@app.route('/admin', methods=['GET'])
def get_admin():
    admin = Admin.query.first()
    if admin:
        return jsonify({'id': admin.id, 'username': admin.username, 'password': admin.password}), 200
    else:
        return jsonify({'message': 'No admin found'}), 404

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Query the admin from the database
    admin = Admin.query.filter_by(username=username).first()

    if admin and admin.password == password:
        return jsonify({'success': True, 'message': 'Login successful'}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    try:
        game = Game.query.get_or_404(game_id)
        db.session.delete(game)
        db.session.commit()
        return jsonify({'message': 'Game deleted successfully'}), 200
    except Exception as e:
        return jsonify({
            'error': 'Failed to delete game',
            'message': str(e)
        }), 500

# Add a new customer
@app.route('/api/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    if not data or not 'name' in data or not 'email' in data or not 'phone' in data:
        abort(400, description="Invalid data: Name, email, and phone are required.")

    # Check if customer already exists
    if find_customer(data['email']):
        abort(400, description="Customer with this email already exists.")

    # Add the new customer to the database
    new_customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully', 'customer': {
        'id': new_customer.id,
        'name': new_customer.name,
        'email': new_customer.email,
        'phone': new_customer.phone
    }}), 201

# Get all customers
@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    customers_list = [{
        'id': customer.id,
        'name': customer.name,
        'email': customer.email,
        'phone': customer.phone
    } for customer in customers]
    return jsonify(customers_list), 200

# Delete a customer by email
@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully'}), 200
    except Exception as e:
        return jsonify({
            'error': 'Failed to delete customer',
            'message': str(e)
        }), 500

# Error handler for 400
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400

@app.route('/loan', methods=['POST'])
def loan_game():
    print("🚀 Loan request received")  # Debug log
    data = request.json
    print("📩 Received data:", data)  # Print received data

    game_id = data.get('game_id')
    customer_id = data.get('customer_id')

    if not game_id or not customer_id:
        print("❌ Missing game_id or customer_id")  # Debug log
        return jsonify({"error": "Missing game_id or customer_id"}), 400

    game = Game.query.filter_by(id=game_id).first()
    if not game:
        print("❌ Game not found")  # Debug log
        return jsonify({"error": "Game not found"}), 404

    if game.quantity < 1:
        print("❌ Game not available")  # Debug log
        return jsonify({"error": "Game not available"}), 400

    # Loan game
    new_loan = Loan(game_id=game_id, customer_id=customer_id)
    game.quantity -= 1  # Reduce stock
    db.session.add(new_loan)
    db.session.commit()
    
    print("✅ Game loaned successfully")  # Debug log
    return jsonify({"message": "Game loaned successfully"}), 201

@app.route('/loans', methods=['GET'])
def get_loans():
    loans = Loan.query.all()
    loan_list = []
    for loan in loans:
        loan_list.append({
            "id": loan.id,
            "game_id": loan.game_id,
            "customer_id": loan.customer_id,
            "loan_date": loan.loan_date,
            "return_date": loan.return_date
        })
    return jsonify(loan_list)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all database tables defined in your models (check the models folder)

    with app.test_client() as test:
        # GET test here
        get_response = test.get('/games')
        print("\nTesting GET /games endpoint:")
        print(f"Response: {get_response.data}")
        get_response = test.get('/admin')
        print("\nTesting GET /admin endpoint:")
        print(f"Response: {get_response.data}")

    
    app.run(debug=True)  # start the flask application in debug mode

    # DONT FORGET TO ACTIVATE THE ENV FIRST:
    # /env/Scripts/activate - for windows
    # source ./env/bin/activate - - mac
