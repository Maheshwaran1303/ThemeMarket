
document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".checkout-form");
  const continueBtn = document.querySelector(".continue-btn");

  // ✅ All validation rules
  const fields = {
    first_name: { regex: /^[A-Za-z\s]{2,}$/, message: "Enter a valid name (letters only, min 2 chars)." },
    email: { regex: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, message: "Enter a valid email address." },
    phone_number: { regex: /^\d{6,15}$/, message: "Enter a valid phone number (6–15 digits)." },
    flat_no: { regex: /^.{1,}$/, message: "Flat/House No. cannot be empty." },
    address: { regex: /^.{5,}$/, message: "Address must be at least 5 characters long." },
    city: { regex: /^[A-Za-z\s]{2,}$/, message: "Enter a valid city name." },
    postal_code: { regex: /^[0-9]{4,10}$/, message: "Enter a valid postal code (4–10 digits)." }
  };

  // ✅ Initialize: add <small> error spans
  Object.keys(fields).forEach(name => {
    const input = form.querySelector(`[name="${name}"]`);
    if (input) {
      const msg = document.createElement("small");
      msg.className = "error-msg";
      input.insertAdjacentElement("afterend", msg);

      // Real-time validation
      input.addEventListener("input", () => validateField(input, fields[name], msg));
      input.addEventListener("blur", () => validateField(input, fields[name], msg));
    }
  });

  // ✅ Core validation function
  function validateField(input, rule, msg) {
    const value = input.value.trim();
    if (!value) {
      setInvalid(input, msg, "This field is required.");
    } else if (!rule.regex.test(value)) {
      setInvalid(input, msg, rule.message);
    } else {
      setValid(input, msg);
    }
    checkFormValidity();
  }

  // ✅ Styling handlers
  function setInvalid(input, msg, message) {
    msg.textContent = message;
    input.classList.add("invalid");
    input.classList.remove("valid");
  }

  function setValid(input, msg) {
    msg.textContent = "";
    input.classList.remove("invalid");
    input.classList.add("valid");
  }

  // ✅ Form overall validity checker
  function checkFormValidity() {
    const allValid = Object.keys(fields).every(name => {
      const input = form.querySelector(`[name="${name}"]`);
      return input && input.classList.contains("valid");
    });
    continueBtn.disabled = !allValid;
  }

  // ✅ Real-time email duplicate check (AJAX)
  const emailInput = form.querySelector('[name="email"]');
  if (emailInput) {
    emailInput.addEventListener("blur", () => {
      const email = emailInput.value.trim();
      if (!email || !fields.email.regex.test(email)) return;
      fetch(`/check-email/?email=${email}`)
        .then(res => res.json())
        .then(data => {
          const msg = emailInput.nextElementSibling;
          if (data.exists) {
            setInvalid(emailInput, msg, "This email is already registered. Try logging in.");
          }
          checkFormValidity();
        })
        .catch(err => console.error("Email check error:", err));
    });
  }

  // ✅ Final safety check on submit
  form.addEventListener("submit", function (e) {
    let valid = true;
    Object.keys(fields).forEach(name => {
      const input = form.querySelector(`[name="${name}"]`);
      const msg = input.nextElementSibling;
      if (!fields[name].regex.test(input.value.trim())) {
        setInvalid(input, msg, fields[name].message);
        valid = false;
      }
    });
    if (!valid) {
      e.preventDefault();
      alert("⚠️ Please fix all errors before continuing.");
    }
  });
});
