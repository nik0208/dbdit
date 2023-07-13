document.querySelector(".login-form button").addEventListener("click", function(event) {
    event.preventDefault();
    // Get form input values
    var username = document.querySelector(".login-form input[type='text']").value;
    var password = document.querySelector(".login-form input[type='password']").value;
    // Validate input values
    if (username === "" || password === "") {
        alert("Please enter a username and password.");
    } else {
        alert("Logged in as " + username + ".");
    }
    });