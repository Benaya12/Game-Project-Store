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

checkLoginStatus();