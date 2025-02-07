// Function to handle login
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
            username: username,
            password: password
        });

        if (response.status === 200) {
            alert('Login successful!');
            // Show the main section after successful login
            document.getElementById('auth-section').classList.add('hidden');
            document.getElementById('main-section').classList.remove('hidden');
        }
    } catch (error) {
        console.error('Error logging in:', error);
        alert('Invalid username or password');
    }
}

// Function to handle logout
function logout() {
    // Clear any session data (if applicable)
    // Redirect to the login page
    document.getElementById('auth-section').classList.remove('hidden');
    document.getElementById('main-section').classList.add('hidden');
}

// Function to get all games
async function getGames() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/games');
        const gamesList = document.getElementById('games-list');
        gamesList.innerHTML = ''; // Clear existing list

        response.data.games.forEach(game => {
            gamesList.innerHTML += `
                <div class="game-card">
                    <h3>${game.title}</h3>
                    <p>Genre: ${game.genre}</p>
                    <p>Price: $${game.price}</p>
                    <p>Quantity: ${game.quantity}</p>
                    <p>Loan Status: ${game.loan_status ? 'Loaned' : 'Available'}</p>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching games:', error);
        alert('Failed to load games');
    }
}

// Function to add a new game
async function addGame() {
    const title = document.getElementById('game-title').value;
    const genre = document.getElementById('game-genre').value;
    const price = document.getElementById('game-price').value;
    const quantity = document.getElementById('game-quantity').value;

    try {
        await axios.post('http://127.0.0.1:5000/games', {
            title: title,
            genre: genre,
            price: price,
            quantity: quantity
        });

        // Clear form fields
        document.getElementById('game-title').value = '';
        document.getElementById('game-genre').value = '';
        document.getElementById('game-price').value = '';
        document.getElementById('game-quantity').value = '';

        // Refresh the games list
        getGames();

        alert('Game added successfully!');
    } catch (error) {
        console.error('Error adding game:', error);
        alert('Failed to add game');
    }
}

// Function to delete a game
async function deleteGame(gameId) {
    try {
        await axios.delete(`http://127.0.0.1:5000/games/${gameId}`);
        getGames();
        alert('Game deleted successfully!');
    } catch (error) {
        console.error('Error deleting game:', error);
        alert('Failed to delete game');
    }
}

// Function to register a new customer
async function addCustomer() {
    const name = document.getElementById('customer-name').value;
    const email = document.getElementById('customer-email').value;
    const phone = document.getElementById('customer-phone').value;

    try {
        await axios.post('http://127.0.0.1:5000/customers', {
            name: name,
            email: email,
            phone: phone
        });

        // Clear form fields
        document.getElementById('customer-name').value = '';
        document.getElementById('customer-email').value = '';
        document.getElementById('customer-phone').value = '';

        alert('Customer added successfully!');
    } catch (error) {
        console.error('Error adding customer:', error);
        alert('Failed to add customer');
    }
}

// Function to loan a game to a customer
async function createLoan() {
    const gameId = document.getElementById('loan-game-id').value;
    const customerId = document.getElementById('loan-customer-id').value;

    try {
        const response = await axios.post('http://127.0.0.1:5000/loans', {
            game_id: gameId,
            customer_id: customerId
        });

        alert('Game loaned successfully!');
        console.log(response.data);
    } catch (error) {
        console.error('Error loaning game:', error);
        alert('Failed to loan game');
    }
}

// Function to return a loaned game
async function returnLoan(loanId) {
    try {
        const response = await axios.post(`http://127.0.0.1:5000/loans/${loanId}/return`);
        alert('Game returned successfully!');
        console.log(response.data);
    } catch (error) {
        console.error('Error returning loan:', error);
        alert('Failed to return game');
    }
}

// Load all games when the page loads
document.addEventListener('DOMContentLoaded', getGames);
