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
                    <p>Author: ${game.author}</p>
                    <p>Year: ${game.year_published}</p>
                    <p>Type: ${game.types}</p>
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
    const author = document.getElementById('game-author').value;
    const year_published = document.getElementById('game-year-published').value;
    const types = document.getElementById('game-type').value;

    try {
        await axios.post('http://127.0.0.1:5000/games', {
            title: title,
            author: author,
            year_published: year_published,
            types: types
        });
        
        // Clear form fields
        document.getElementById('game-title').value = '';
        document.getElementById('game-author').value = '';
        document.getElementById('game-year-published').value = '';
        document.getElementById('game-type').value = '';

        // Refresh the games list
        getGames();
        
        alert('Game added successfully!');
    } catch (error) {
        console.error('Error adding game:', error);
        alert('Failed to add game');
    }
}

// Load all games when page loads
document.addEventListener('DOMContentLoaded', getGames);