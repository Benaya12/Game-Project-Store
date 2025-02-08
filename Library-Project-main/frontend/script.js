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
                <p>Developer: ${game.developer}</p>
                <p>Year: ${game.year_published}</p>
                <p>Genre: ${game.genres}</p>
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
    const developer = document.getElementById('game-developer').value;
    const year_published = parseInt(document.getElementById('game-year').value);
    const genres = document.getElementById('game-genre').value;

    try {
        await axios.post('http://127.0.0.1:5000/games', {
            title,
            developer,
            year_published,
            genres
        });

        // Save login state before refresh
        sessionStorage.setItem('isLoggedIn', 'true');

        // Refresh the games list without reloading the page
        getGames();

        // Clear the form
        document.getElementById('game-title').value = '';
        document.getElementById('game-developer').value = '';
        document.getElementById('game-year').value = '';
        document.getElementById('game-genre').value = '';

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
        // Refresh the games list after successful deletion
        getGames();
    } catch (error) {
        console.error('Error deleting game:', error);
        alert('Failed to delete game');
    }
}

// Function to handle user login
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
            username: username,
            password: password
        });

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

// Function to handle logout
function logout() {
    sessionStorage.removeItem('isLoggedIn');
    showAuthSection();
}

// Show main section (games) and fetch games
function showMainSection() {
    document.getElementById('auth-section').classList.add('hidden');
    document.getElementById('main-section').classList.remove('hidden');
    getGames();
}

// Show authentication (login) section
function showAuthSection() {
    document.getElementById('auth-section').classList.remove('hidden');
    document.getElementById('main-section').classList.add('hidden');
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    if (sessionStorage.getItem('isLoggedIn') === 'true') {
        showMainSection();
    } else {
        showAuthSection();
    }
    // Now reveal the page smoothly
    document.documentElement.style.visibility = 'visible';
    document.body.style.display = 'block';
});