from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from models import db
from models.game import Game
from models.loan import Loan
from models.admin import Admin


app = Flask(__name__)  # - create a flask instance
# - enable all routes, allow requests from anywhere (optional - not recommended for security)
CORS(app, resources={r"/*": {"origins": "*"}})


# Specifies the database connection URL. In this case, it's creating a SQLite database
# named 'library.db' in your project directory. The three slashes '///' indicate a
# relative path from the current directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db.init_app(app)  # initializes the databsewith the flask application


# this is a decorator from the flask module to define a route for for adding a game, supporting POST requests.(check the decorator summary i sent you and also the exercises)
@app.route('/games', methods=['POST'])
def add_game():
    data = request.json  # Parse the JSON data from the request body
    new_game = Game(
        title=data['title'],
        genre=data['genre'],  # Corrected from 'genres' to 'genre'
        price=data['price'],
        quantity=data['quantity']
    )
    db.session.add(new_game)  # Add the new game to the session
    db.session.commit()  # Commit the session to save the game to the database
    return jsonify({'message': 'Game added to database.'}), 201

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
                'quantity': game.quantity
            }
            games_list.append(game_data)  # Add the iterated game dictionary to our list

        return jsonify({
            'message': 'games retrieved successfully',
            'games': games_list
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve games',
            'message': str(e)
        }), 500
                              #

@app.route('/admin',methods=['GET'])
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all database tables defined in your  models(check the models folder)
        
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