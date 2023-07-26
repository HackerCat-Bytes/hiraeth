// Get the login form, sign up form, their buttons and close buttons
var loginForm = document.getElementById('login');
var signUpForm = document.getElementById('signUp');
var loginButton = document.getElementById('loginButton');
var signUpButton = document.getElementById('signUpButton');
var loginCloseButton = document.getElementById('loginCloseButton');
var signUpCloseButton = document.getElementById('signUpCloseButton');

// When the login button is clicked, remove the 'hidden' class from the login form
loginButton.addEventListener('click', function() {
    loginForm.classList.remove('hidden')
});

// When the sign up button is clicked, remove the 'hidden' class from the sign up form
signUpButton.addEventListener('click', function() {
    signUpForm.classList.remove('hidden')
});

// When the close button is clicked on login form, add the 'hidden' class back to the login form
loginCloseButton.addEventListener('click', function() {
    loginForm.classList.add('hidden')
});

// When the close button is clicked on sign up form, add the 'hidden' class back to the sign up form
signUpCloseButton.addEventListener('click', function() {
    signUpForm.classList.add('hidden')
});

// Get the 'go to sign up' and 'go to login' links
var goToSignUp = document.getElementById('goToSignUp');
var goToLogin = document.getElementById('goToLogin');

// When the 'go to sign up' link is clicked, hide the login form and show the sign up form
goToSignUp.addEventListener('click', function(event) {
    event.preventDefault(); // prevent the link from jumping to the top of the page
    loginForm.classList.add('hidden');
    signUpForm.classList.remove('hidden');
});

// When the 'go to login' link is clicked, hide the sign up form and show the login form
goToLogin.addEventListener('click', function(event) {
    event.preventDefault(); // prevent the link from jumping to the top of the page
    signUpForm.classList.add('hidden');
    loginForm.classList.remove('hidden');
});

// Assume the form submission is successful
loginForm.onsubmit = function(e) {
    e.preventDefault(); // prevent default form submission
    sessionStorage.setItem('isLoggedIn', 'true');
    alert('Logged in successfully!'); // alert the user
    loginForm.classList.add('hidden'); // hide the form
    loginButton.style.display = 'none'; // hide the button
    signUpButton.style.display = 'none'; // hide the button
}

signUpForm.onsubmit = function(e) {
    e.preventDefault(); // prevent default form submission
    sessionStorage.setItem('isLoggedIn', 'true');
    alert('Signed up and logged in successfully!'); // alert the user
    signUpForm.classList.add('hidden'); // hide the form
    loginButton.style.display = 'none'; // hide the button
    signUpButton.style.display = 'none'; // hide the button
}

// This runs once the page is fully loaded
// It hides the sign up and log in buttons after a user has registered/logged in
window.onload = function() {
    if (sessionStorage.getItem('isLoggedIn')) {
        loginButton.style.display = 'none';
        signUpButton.style.display = 'none';
    }
}