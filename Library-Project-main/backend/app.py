from flask import Flask, request, jsonify, session
from flask_cors import CORS
from datetime import datetime
from models import db
from models.admin import Admin
from models.game import Game
from models.customer import Customer
from models.loan import Loan
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)  # Create a Flask instance
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Required for session management
db.init_app(app)  # Initialize the database with the Flask app

# Create all database tables within the application context
with app.app_context():
    db.create_all()

# Error handler for unauthorized access
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized access'}), 401

# Admin Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    admin = Admin.query.filter_by(username=username).first()

    if admin and check_password_hash(admin.password, password):
        session['admin_id'] = admin.id  # Store admin ID in session
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

# Admin Logout Route
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('admin_id', None)  # Remove admin ID from session
    return jsonify({'message': 'Logout successful'}), 200

# Check Admin Session Route
@app.route('/check-session', methods=['GET'])
def check_session():
    if 'admin_id' in session:
        admin = Admin.query.get(session['admin_id'])
        return jsonify({'message': 'Admin is logged in', 'admin': admin.username}), 200
    else:
        return jsonify({'error': 'Admin is not logged in'}), 401

# Add Admin Route
@app.route('/add-admin', methods=['POST'])
def add_admin():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    existing_admin = Admin.query.filter_by(username=username).first()
    if existing_admin:
        return jsonify({'error': 'Admin already exists'}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    new_admin = Admin(username=username, password=hashed_password)
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({'message': 'Admin added successfully'}), 201

# Add Game Route
@app.route('/games', methods=['POST'])
def add_game():
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401

    data = request.json
    new_game = Game(
        title=data['title'],
        genre=data['genre'],
        price=data['price'],
        quantity=data['quantity']
    )
    db.session.add(new_game)
    db.session.commit()
    return jsonify({'message': 'Game added to database.'}), 201

# Get All Games Route
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

# Delete Game Route
@app.route('/games/<int:id>', methods=['DELETE'])
def delete_game(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401

    game = Game.query.get_or_404(id)
    db.session.delete(game)
    db.session.commit()
    return jsonify({'message': 'Game deleted successfully.'}), 200

# Add Customer Route
@app.route('/customers', methods=['POST'])
def add_customer():
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401

    data = request.json
    new_customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully.'}), 201

# Get All Customers Route
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

# Add Loan Route
@app.route('/loans', methods=['POST'])
def add_loan():
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401

    data = request.json
    game_id = data.get('game_id')
    customer_id = data.get('customer_id')

    # Check if the game exists and is available
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    if game.loan_status:
        return jsonify({'error': 'Game is already loaned'}), 400

    # Update game loan status
    game.loan_status = True
    db.session.commit()

    # Create a new loan record
    new_loan = Loan(
        game_id=game_id,
        customer_id=customer_id
    )
    db.session.add(new_loan)
    db.session.commit()

    return jsonify({'message': 'Game loaned successfully'}), 201

# Return Loan Route
@app.route('/loans/<int:loan_id>/return', methods=['PUT'])
def return_loan(loan_id):
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401

    loan = Loan.query.get_or_404(loan_id)
    game = Game.query.get(loan.game_id)

    # Update game loan status
    game.loan_status = False
    loan.return_date = datetime.utcnow()
    db.session.commit()

    return jsonify({'message': 'Game returned successfully'}), 200

# Get All Loaned Games Route
@app.route('/loans', methods=['GET'])
def get_loans():
    loans = Loan.query.filter_by(return_date=None).all()  # Only active loans
    loaned_games = []

    for loan in loans:
        game = Game.query.get(loan.game_id)
        customer = Customer.query.get(loan.customer_id)
        loaned_games.append({
            'loan_id': loan.id,
            'game_title': game.title,
            'customer_name': customer.name,
            'loan_date': loan.loan_date
        })

    return jsonify({
        'message': 'Loaned games retrieved successfully',
        'loaned_games': loaned_games
    }), 200

# Run the application
if __name__ == '__main__':
    app.run(debug=True)