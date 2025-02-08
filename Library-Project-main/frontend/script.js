// function to get all games from the API
async function getGames() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/games');
        const gamesList = document.getElementById('games-list');
        gamesList.innerHTML = ''; // Clear existing list

        response.data.games.forEach(game => {
            gamesList.innerHTML += `
                <div class="game-card">
                    <h3>${game.title}</h3>
                    <p>Developer: ${game.developer}</p>
                    <p>Year: ${game.year_published}</p>
                    <p>Genre: ${game.generes}</p>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching games:', error);
        alert('Failed to load games');
    }
}

// function to add a new game to the database
async function addGame() {
    const title = document.getElementById('game-title').value;
    const developer = document.getElementById('game-developer').value;
    const year_published = document.getElementById('game-year-published').value;
    const generes = document.getElementById('game-genres').value;

    try {
        await axios.post('http://127.0.0.1:5000/games', {
            title: title,
            developer: developer,
            year_published: year_published,
            generes: generes
        });
        
        // Clear form fields
        document.getElementById('game-title').value = '';
        document.getElementById('game-developer').value = '';
        document.getElementById('game-year-published').value = '';
        document.getElementById('game-genres').value = '';

        // Refresh the games list
        getGames();
        
        alert('Game added successfully!');
    } catch (error) {
        console.error('Error adding game:', error);
        alert('Failed to add game');
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
            document.getElementById('auth-section').classList.add('hidden');
            document.getElementById('main-section').classList.remove('hidden');
            getGames();
        } else {

            alert('Invalid credentials');
        }
    } catch (error) {

        console.error('Error logging in:', error);
        alert('Failed to login');
    }
}

//Function to handle user registration

// Function to handle logout
function logout() {
    document.getElementById('auth-section').classList.remove('hidden');
    document.getElementById('main-section').classList.add('hidden');
}

// Load all games when page loads
document.addEventListener('DOMContentLoaded', getGames);

// Function to add a new game to the database
async function addGame() {
    const title = document.getElementById('game-title').value;
    const genre = document.getElementById('game-genre').value;  // Corrected from 'generes' to 'genre'
    const price = parseFloat(document.getElementById('game-price').value);  // Ensure price is a float
    const quantity = parseInt(document.getElementById('game-quantity').value, 10);  // Ensure quantity is an integer

    try {
        await axios.post('http://127.0.0.1:5000/games', {
            title: title,
            genre: genre,  // Corrected from 'generes' to 'genre'
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


// Function to get all games from the API
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
                    <p>Price: $${game.price.toFixed(2)}</p>
                    <p>Quantity: ${game.quantity}</p>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching games:', error);
        alert('Failed to load games');
    }
}
