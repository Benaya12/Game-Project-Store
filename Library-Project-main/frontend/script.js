// Function to handle admin login
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
            alert('Login successful!');
            checkSession();  // Check session status after login
        }
    } catch (error) {
        const message = error.response?.data?.error || 'Login failed. Please try again.';
        alert(message);
    }
}

// Function to handle admin logout
async function logout() {
    try {
        const response = await axios.post('http://127.0.0.1:5000/logout');
        if (response.status === 200) {
            alert('Logout successful!');
            window.location.href = '/';  // Redirect to login page
        }
    } catch (error) {
        console.error('Error logging out:', error);
        alert('Failed to logout');
    }
}

// Function to check admin session status
async function checkSession() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/check-session');
        if (response.status === 200) {
            document.getElementById('auth-section').classList.add('hidden');
            document.getElementById('main-section').classList.remove('hidden');
        }
    } catch (error) {
        document.getElementById('auth-section').classList.remove('hidden');
        document.getElementById('main-section').classList.add('hidden');
    }
}

// Check session status on page load
checkSession();