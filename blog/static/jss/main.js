

// File: app.js

// Logout functionality
function logout() {
    // Clear user session (example with local storage)
    localStorage.removeItem('userToken'); // or session token
    alert('You have been logged out');
    
    // Redirect to login page
    window.location.href = 'login.html';
}

// Add event listener to Logout button if it's available
document.querySelector('a[href="logout.html"]')?.addEventListener('click', function(e) {
    e.preventDefault();  // Prevent actual page navigation
    logout();  // Call the logout function
});