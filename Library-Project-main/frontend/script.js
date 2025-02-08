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
            genre,  // Removed 'genres' -> should be 'genre'
            price,
            quantity
        });

        // Refresh the games list
        getGames();

        // Clear the form fields
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

function addCustomer() {
    const name = document.getElementById('customer-name').value;
    const email = document.getElementById('customer-email').value;
    const phone = document.getElementById('customer-phone').value;
  
    if (name && email && phone) {
      const customer = { name, email, phone };
      // Save the customer (e.g., to localStorage or a backend API)
      saveCustomer(customer);
      // Clear the form
      document.getElementById('customer-name').value = '';
      document.getElementById('customer-email').value = '';
      document.getElementById('customer-phone').value = '';
      // Refresh the customers list
      displayCustomers();
    } else {
      alert('Please fill in all fields.');
    }
  }
  
  function saveCustomer(customer) {
    // Example: Save to localStorage
    const customers = JSON.parse(localStorage.getItem('customers')) || [];
    customers.push(customer);
    localStorage.setItem('customers', JSON.stringify(customers));
  }
  
  function displayCustomers() {
    const customers = JSON.parse(localStorage.getItem('customers')) || [];
    const customersList = document.getElementById('customers-list');
    customersList.innerHTML = '';
  
    customers.forEach(customer => {
      const customerCard = document.createElement('div');
      customerCard.className = 'customer-card';
      customerCard.innerHTML = `
        <h3>${customer.name}</h3>
        <p>Email: ${customer.email}</p>
        <p>Phone: ${customer.phone}</p>
        <button class="delete-btn" onclick="deleteCustomer('${customer.email}')">Delete</button>
      `;
      customersList.appendChild(customerCard);
    });
  }
  
  function deleteCustomer(email) {
    let customers = JSON.parse(localStorage.getItem('customers')) || [];
    customers = customers.filter(customer => customer.email !== email);
    localStorage.setItem('customers', JSON.stringify(customers));
    displayCustomers();
  }
  
  // Call displayCustomers() when the page loads or after login