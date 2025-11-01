// Switch between forms
document.getElementById("switchToLogin").onclick = function() {
  document.getElementById("registerForm").classList.remove("active");
  document.getElementById("loginForm").classList.add("active");
};
document.getElementById("switchToRegister").onclick = function() {
  document.getElementById("loginForm").classList.remove("active");
  document.getElementById("registerForm").classList.add("active");
};

// Helper: show alert
function showAlert(message, type = "success") {
  const alertBox = document.getElementById("formAlert");
  alertBox.textContent = message;
  alertBox.className = `form-alert show ${type}`;
  setTimeout(() => {
    alertBox.classList.remove("show");
  }, 3000);
}

// === Real-time Register Validation ===
const regName = document.getElementById("reg-username");
const regEmail = document.getElementById("reg-email");
const regPass = document.getElementById("reg-password");

// Regex patterns
const nameRegex = /^[A-Za-z\s]{3,}$/;
const emailRegex = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

// Event listeners
regName.addEventListener("input", () => {
  if (!nameRegex.test(regName.value.trim())) {
    regName.classList.add("input-error");
    regName.classList.remove("input-success");
    document.getElementById("reg-name-error").textContent =
      "Enter a valid name (letters only, min 3 chars)";
  } else {
    regName.classList.remove("input-error");
    regName.classList.add("input-success");
    document.getElementById("reg-name-error").textContent = "";
  }
});

// Email availability check (real-time)

regEmail.addEventListener("input", () => {
  const email = regEmail.value.trim();
  const emailRegex = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

  if (!emailRegex.test(email)) {
    regEmail.classList.add("input-error");
    regEmail.classList.remove("input-success");
    document.getElementById("reg-email-error").textContent = "Invalid email format";
    return;
  }

  // ✅ Check email availability via AJAX
  fetch(`/check-email/?email=${encodeURIComponent(email)}`)
    .then(response => response.json())
    .then(data => {
      if (data.exists) {
        regEmail.classList.add("input-error");
        regEmail.classList.remove("input-success");
        document.getElementById("reg-email-error").textContent =
          "Email already registered. Try logging in.";
      } else {
        regEmail.classList.remove("input-error");
        regEmail.classList.add("input-success");
        document.getElementById("reg-email-error").textContent = "";
      }
    })
    .catch(() => {
      console.error("Error checking email availability.");
    });
});

regPass.addEventListener("input", () => {
  if (regPass.value.length < 6) {
    regPass.classList.add("input-error");
    regPass.classList.remove("input-success");
    document.getElementById("reg-pass-error").textContent =
      "Password must be at least 6 characters";
  } else {
    regPass.classList.remove("input-error");
    regPass.classList.add("input-success");
    document.getElementById("reg-pass-error").textContent = "";
  }
});

// === Submit Validation (Register) ===
function validateRegisterForm(event) {
  let valid = true;

  if (!nameRegex.test(regName.value.trim())) valid = false;
  if (!emailRegex.test(regEmail.value.trim())) valid = false;
  if (regPass.value.length < 6) valid = false;

  if (!valid) {
    event.preventDefault();
    showAlert("Please correct the highlighted fields.", "error");
  } else {
    showAlert("Registration successful!", "success");
  }

  return valid;
}

// === Real-time Login Validation ===
const loginEmail = document.getElementById("login-email");
const loginPass = document.getElementById("login-password");

loginEmail.addEventListener("input", () => {
  if (!emailRegex.test(loginEmail.value.trim())) {
    loginEmail.classList.add("input-error");
    document.getElementById("login-email-error").textContent = "Invalid email";
  } else {
    loginEmail.classList.remove("input-error");
    document.getElementById("login-email-error").textContent = "";
  }
});

loginPass.addEventListener("input", () => {
  if (loginPass.value.length < 6) {
    loginPass.classList.add("input-error");
    document.getElementById("login-pass-error").textContent =
      "Password too short";
  } else {
    loginPass.classList.remove("input-error");
    document.getElementById("login-pass-error").textContent = "";
  }
});

// === Login Submit ===
function validateLoginForm(event) {
  let valid = true;
  if (!emailRegex.test(loginEmail.value.trim()) || loginPass.value.length < 6) {
    valid = false;
    showAlert("Invalid login credentials.", "error");
  } else {
    showAlert("Login successful!", "success");
  }

  if (!valid) event.preventDefault();
  return valid;
}
