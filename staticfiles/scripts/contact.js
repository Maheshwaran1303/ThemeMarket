document.querySelector(".contact-form").addEventListener("submit", function(e) {
  const first = document.getElementById("first_name").value.trim();
  const email = document.getElementById("email").value.trim();
  const message = document.getElementById("message").value.trim();

  if (!first || !email || !message) {
    e.preventDefault();
    alert("Please fill in all required fields!");
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
