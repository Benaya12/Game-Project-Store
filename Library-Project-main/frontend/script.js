// Function to handle login
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
        alert('Please enter both username and password');
        return;
    }

    try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
            username: username,
            password: password
        });

        if (response.status === 200) {
            localStorage.setItem('isLoggedIn', 'true');
            document.getElementById('auth-section').classList.add('hidden');
            document.getElementById('main-section').classList.remove('hidden');
            getGames();
            getLoanedGames();  // Load loaned games on login
        }
    } catch (error) {
        const message = error.response?.data?.error || 'Login failed. Please try again.';
        alert(message);
    }
}

function checkLoginStatus() {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    document.getElementById('auth-section').classList.toggle('hidden', isLoggedIn);
    document.getElementById('main-section').classList.toggle('hidden', !isLoggedIn);
    if (isLoggedIn) {
        getGames();
        getLoanedGames();  // Load loaned games if already logged in
    }
}

function logout() {
    localStorage.removeItem('isLoggedIn');
    checkLoginStatus();
}

async function getGames() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/games');
        const gamesList = document.getElementById('games-list');
        gamesList.innerHTML = '';

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

async function addGame() {
    const title = document.getElementById('game-title').value;
    const genre = document.getElementById('game-genre').value;
    const price = document.getElementById('game-price').value;
    const quantity = document.getElementById('game-quantity').value;

    try {
        const response = await axios.post('http://127.0.0.1:5000/games', {
            title: title,
            genre: genre,
            price: price,
            quantity: quantity
        });

        alert('Game added successfully!');
        getGames();
    } catch (error) {
        console.error('Error adding game:', error);
        alert('Failed to add game');
    }
}

async function addLoan() {
    const gameId = document.getElementById('loan-game-id').value;
    const customerId = document.getElementById('loan-customer-id').value;

    try {
        const response = await axios.post('http://127.0.0.1:5000/loans', {
            game_id: gameId,
            customer_id: customerId
        });

        alert('Game loaned successfully!');
        getLoanedGames();  // Refresh the loaned games list
    } catch (error) {
        console.error('Error loaning game:', error);
        alert('Failed to loan game');
    }
}

async function returnLoan(loanId) {
    try {
        const response = await axios.put(`http://127.0.0.1:5000/loans/${loanId}/return`);
        alert('Game returned successfully!');
        getLoanedGames();  // Refresh the loaned games list
    } catch (error) {
        console.error('Error returning game:', error);
        alert('Failed to return game');
    }
}

async function getLoanedGames() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/loans');
        const loanedGamesList = document.getElementById('loaned-games-list');
        loanedGamesList.innerHTML = '';

        response.data.loaned_games.forEach(loan => {
            loanedGamesList.innerHTML += `
                <div class="loan-card">
                    <h3>${loan.game_title}</h3>
                    <p>Loaned by: ${loan.customer_name}</p>
                    <p>Loan Date: ${new Date(loan.loan_date).toLocaleDateString()}</p>
                    <button onclick="returnLoan(${loan.loan_id})">Return Game</button>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching loaned games:', error);
        alert('Failed to load loaned games');
    }
}

checkLoginStatus();