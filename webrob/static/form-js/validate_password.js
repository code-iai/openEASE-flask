var myInput = document.getElementById("psw");
var letter = document.getElementById("letter");
var capital = document.getElementById("capital");
var number = document.getElementById("number");
var length = document.getElementById("length");
var check = document.getElementById("retype_password");

// mySubmit.onclick = function() {
//   document.getElementById("message").style.display = "block";
// }

// When the user clicks on the password field, show the message box
myInput.onfocus = function () {
    document.getElementById("message").style.display = "block";
    document.getElementById("psw-check").style.display = "none";
}

// When the user clicks outside of the password field, hide the message box
myInput.onblur = function () {
    document.getElementById("message").style.display = "none";
    // document.getElementById("psw-check").style.display = "block";
}

// When the user starts to type something inside the password field
myInput.onkeyup = function () {
    // Validate lowercase letters

    var lowerCaseLetters = /[a-z]/g;
    if (myInput.value.match(lowerCaseLetters)) {
        letter.classList.remove("invalid");
        letter.classList.add("valid");
    } else {
        letter.classList.remove("valid");
        letter.classList.add("invalid");
    }

    // Validate capital letters
    var upperCaseLetters = /[A-Z]/g;
    if (myInput.value.match(upperCaseLetters)) {
        capital.classList.remove("invalid");
        capital.classList.add("valid");
    } else {
        capital.classList.remove("valid");
        capital.classList.add("invalid");
    }

    // Validate numbers
    var numbers = /[0-9]/g;
    if (myInput.value.match(numbers)) {
        number.classList.remove("invalid");
        number.classList.add("valid");
    } else {
        number.classList.remove("valid");
        number.classList.add("invalid");
    }

    // Validate length
    if (myInput.value.length >= 6) {
        length.classList.remove("invalid");
        length.classList.add("valid");
    } else {
        length.classList.remove("valid");
        length.classList.add("invalid");
    }
}

// check if password and confirm password fields match


check.onkeyup = function () {
    if (document.getElementById('psw').value == document.getElementById('retype_password').value) {
        document.getElementById('invalid-msg').style.color = 'green';
        document.getElementById('invalid-msg').innerHTML = 'matching';
    } else {
        document.getElementById('invalid-msg').style.color = 'red';
        document.getElementById('invalid-msg').innerHTML = 'not matching';
    }
}