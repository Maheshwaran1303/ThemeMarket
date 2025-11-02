document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".contact-form");
  const inputs = form.querySelectorAll("input, textarea");
  const container = document.querySelector(".container");

  const rules = {
    first_name: {
      required: true,
      pattern: /^[A-Za-z\s]+$/,
      message: "First name should contain only letters.",
    },
    last_name: {
      required: false,
      pattern: /^[A-Za-z\s]+$/,
      message: "Last name should contain only letters.",
    },
    email: {
      required: true,
      pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      message: "Enter a valid email address.",
    },
    message: {
      required: true,
      minLength: 10,
      message: "Message must be at least 10 characters long.",
    },
  };

  // Real-time validation
  inputs.forEach((input) => {
    input.addEventListener("input", () => validateField(input));
    input.addEventListener("blur", () => validateField(input));
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    let valid = true;
    clearErrors();

    inputs.forEach((input) => {
      if (!validateField(input)) valid = false;
    });

    if (valid) {
      // ✅ Show success message
      showSuccessMessage();
      form.reset();
      clearErrors();
    }
  });

  function validateField(input) {
    const name = input.getAttribute("name");
    const value = input.value.trim();
    const rule = rules[name];
    if (!rule) return true;

    clearError(input);

    if (rule.required && value === "") {
      showError(input, `${formatLabel(name)} is required.`);
      return false;
    }

    if (rule.pattern && value && !rule.pattern.test(value)) {
      showError(input, rule.message);
      return false;
    }

    if (rule.minLength && value.length < rule.minLength) {
      showError(input, rule.message);
      return false;
    }

    showSuccess(input);
    return true;
  }

  function showError(input, message) {
    const error = document.createElement("small");
    error.className = "error-text";
    error.textContent = message;
    input.parentElement.appendChild(error);
    input.classList.remove("success-border");
    input.classList.add("error-border");
  }

  function showSuccess(input) {
    input.classList.remove("error-border");
    input.classList.add("success-border");
  }

  function clearErrors() {
    document.querySelectorAll(".error-text").forEach((el) => el.remove());
    inputs.forEach((input) =>
      input.classList.remove("error-border", "success-border")
    );
  }

  function clearError(input) {
    const error = input.parentElement.querySelector(".error-text");
    if (error) error.remove();
    input.classList.remove("error-border", "success-border");
  }

  function formatLabel(name) {
    return name
      .replace(/_/g, " ")
      .replace(/\b\w/g, (char) => char.toUpperCase());
  }

  // ✅ Success message with checkmark animation
  function showSuccessMessage() {
    const messageBox = document.createElement("div");
    messageBox.className = "success-popup";
    messageBox.innerHTML = `
      <div class="checkmark">
        <svg viewBox="0 0 52 52">
          <circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none"/>
          <path class="checkmark-check" fill="none" d="M14 27l7 7 16-16"/>
        </svg>
      </div>
      <p>Message sent successfully!</p>
    `;
    container.appendChild(messageBox);

    // Auto remove after 3 seconds
    setTimeout(() => {
      messageBox.classList.add("fade-out");
      setTimeout(() => messageBox.remove(), 500);
    }, 3000);
  }
});



// ===============================
// FAQ TOGGLE FUNCTIONALITY
// ===============================

// ===============================
// FAQ TOGGLE FUNCTIONALITY
// ===============================

document.addEventListener("DOMContentLoaded", function () {
  const faqItems = document.querySelectorAll(".faq-item");

  if (faqItems.length === 0) {
    console.warn("⚠️ No FAQ items found. Check your class names in HTML.");
    return;
  }

  faqItems.forEach((item) => {
    const question = item.querySelector(".faq-question");

    if (!question) return;

    question.addEventListener("click", function () {
      // Close all other active FAQ items
      faqItems.forEach((faq) => {
        if (faq !== item) faq.classList.remove("active");
      });

      // Toggle the current one
      item.classList.toggle("active");
    });
  });
});
