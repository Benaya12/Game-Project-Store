// Hide everything until we confirm login state
document.documentElement.style.visibility = 'hidden';
document.body.style.display = 'none';

// Function to get all games from the API
async function getGames() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/games');
        const gamesList = document.getElementById('games-list');
        gamesList.innerHTML = ''; // Clear existing list

        response.data.games.forEach(game => {
            const gameCard = document.createElement('div');
            gameCard.className = 'game-card';
            gameCard.innerHTML = `
                <h3>${game.title}</h3>
                <p>Id: ${game.id}</p>
                <p>Genre: ${game.genre}</p>
                <p>Price: $${game.price}</p>
                <p>Quantity: ${game.quantity}</p>
                <p>Loan Status: ${game.loan_status ? 'Loaned' : 'Available'}</p>
                <button class="delete-btn" onclick="deleteGame(${game.id})">Delete Game</button>
            `;
            gamesList.appendChild(gameCard);
        });
    } catch (error) {
        console.error('Error fetching games:', error);
        alert('Failed to load games');
    }
}

// Function to add a new game to the database
async function addGame() {
    const title = document.getElementById('game-title').value;
    const genre = document.getElementById('game-genre').value;
    const price = parseFloat(document.getElementById('game-price').value);
    const quantity = parseInt(document.getElementById('game-quantity').value);

    try {
        await axios.post('http://127.0.0.1:5000/games', {
            title,
            genre,
            price,
            quantity
        });

        getGames(); // Refresh game list

        // Clear form fields
        document.getElementById('game-title').value = '';
        document.getElementById('game-genre').value = '';
        document.getElementById('game-price').value = '';
        document.getElementById('game-quantity').value = '';

    } catch (error) {
        console.error('Error adding game:', error);
        alert('Failed to add game');
    }
}

// Function to delete a game
async function deleteGame(gameId) {
    if (!confirm('Are you sure you want to delete this game?')) {
        return;
    }

    try {
        await axios.delete(`http://127.0.0.1:5000/games/${gameId}`);
        getGames(); // Refresh the games list
    } catch (error) {
        console.error('Error deleting game:', error);
        alert('Failed to delete game');
    }
}

// Function to handle login
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await axios.post('http://127.0.0.1:5000/login', { username, password });

        if (response.data.success) {
            sessionStorage.setItem('isLoggedIn', 'true');
            showMainSection();
        } else {
            alert('Invalid credentials');
        }
    } catch (error) {
        console.error('Error logging in:', error);
        alert('Failed to login');
    }
}

// Logout function
function logout() {
    sessionStorage.removeItem('isLoggedIn');
    showAuthSection();
}

// Show main section (games) and fetch games
function showMainSection() {
    document.getElementById('auth-section').classList.add('hidden');
    document.getElementById('main-section').classList.remove('hidden');
    getGames();
    getCustomers();
    fetchLoans();
}

// Show authentication (login) section
function showAuthSection() {
    document.getElementById('auth-section').classList.remove('hidden');
    document.getElementById('main-section').classList.add('hidden');
}

// Function to get all customers
async function getCustomers() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/api/customers');
        const customersList = document.getElementById('customers-list');
        customersList.innerHTML = '';

        response.data.forEach(customer => {
            const customerCard = document.createElement('div');
            customerCard.className = 'customer-card';
            customerCard.innerHTML = `
                <h3>${customer.name}</h3>
                <p>Id: ${customer.id}</p>
                <p>Email: ${customer.email}</p>
                <p>Phone: ${customer.phone}</p>
                <button class="delete-btn" onclick="deleteCustomer(${customer.id})">Delete</button>
            `;
            customersList.appendChild(customerCard);
        });
    } catch (error) {
        console.error('Error fetching customers:', error);
        alert('Failed to load customers');
    }
}

// Function to add a new customer
async function addCustomer() {
    const name = document.getElementById('customer-name').value;
    const email = document.getElementById('customer-email').value;
    const phone = document.getElementById('customer-phone').value;

    try {
        await axios.post('http://127.0.0.1:5000/api/customers', { name, email, phone });
        getCustomers(); // Refresh list

        // Clear input fields
        document.getElementById('customer-name').value = '';
        document.getElementById('customer-email').value = '';
        document.getElementById('customer-phone').value = '';
    } catch (error) {
        console.error('Error adding customer:', error);
        alert('Failed to add customer');
    }
}

// Function to delete a customer
async function deleteCustomer(customerId) {
    if (!confirm('Are you sure you want to delete this customer?')) {
        return;
    }

    try {
        await axios.delete(`http://127.0.0.1:5000/customers/${customerId}`);
        getCustomers(); // Refresh customer list
    } catch (error) {
        console.error('Error deleting customer:', error);
        alert('Failed to delete customer');
    }
}

// Function to loan a game
async function loanGame() {
    const gameId = document.getElementById('loan-game-id').value;
    const customerId = document.getElementById('loan-customer-id').value;

    if (!gameId || !customerId) {
        alert("Please enter both game ID and customer ID.");
        return;
    }

    try {
        const response = await axios.post('http://127.0.0.1:5000/loan', { game_id: gameId, customer_id: customerId });

        alert(response.data.message);

        // Clear input fields
        document.getElementById('loan-game-id').value = '';
        document.getElementById('loan-customer-id').value = '';

        fetchLoans(); // Refresh loans list
    } catch (error) {
        console.error('Error loaning game:', error.response || error);
        alert('Error loaning game, please try again.');
    }
}

// Function to fetch active loans
async function fetchLoans() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/loans');

        const loanList = document.getElementById('active-loans-list');
        loanList.innerHTML = '';

        response.data.forEach(loan => {
            const loanItem = document.createElement('div');
            loanItem.classList.add('loan-card');
            loanItem.innerHTML = `
                <p><strong>Loan ID:</strong> ${loan.id}</p>
                <p><strong>Game ID:</strong> ${loan.game_id}</p>
                <p><strong>Customer ID:</strong> ${loan.customer_id}</p>
                <p><strong>Loan Date:</strong> ${loan.loan_date}</p>
                <p><strong>Return Date:</strong> ${loan.return_date || 'Not specified'}</p>
            `;
            loanList.appendChild(loanItem);
        });
    } catch (error) {
        console.error('Error fetching loans:', error);
        alert('Failed to load loans.');
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    if (sessionStorage.getItem('isLoggedIn') === 'true') {
        showMainSection();
    } else {
        showAuthSection();
    }

    document.documentElement.style.visibility = 'visible';
    document.body.style.display = 'block';
});

async function returnGame() {
    const loanId = document.getElementById('return-loan-id').value.trim();

    if (!loanId) {
        alert('Please enter a valid Loan ID.');
        return;
    }

    try {
        const response = await axios.post('http://127.0.0.1:5000/return', {
            loan_id: parseInt(loanId)
        });

        alert(response.data.message);

        // Clear input field
        document.getElementById('return-loan-id').value = '';

        fetchLoans(); // Refresh the active loans list
        getGames();   // Refresh the games list to update availability
    } catch (error) {
        console.error('Error returning game:', error.response?.data || error);
        alert(error.response?.data?.error || 'Failed to return game. Please try again.');
    }
}

async function deleteAllLoans() {
    if (!confirm("Are you sure you want to delete ALL loans? This cannot be undone!")) return;

    try {
        const response = await axios.delete("http://127.0.0.1:5000/loans/reset");
        alert(response.data.message);
        fetchLoans();  // Refresh the loan list
    } catch (error) {
        console.error("Error deleting all loans:", error);
        alert("Failed to delete all loans.");
    }
}

