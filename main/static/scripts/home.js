document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".trending-card");
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("fadeInUp");
      }
    });
  }, { threshold: 0.2 });

  cards.forEach((card) => observer.observe(card));
});


// Trusted By Million Section
document.querySelectorAll('.trusted-number').forEach(num => {
  const value = num.textContent.replace(/[^\d]/g, '');
  let count = 0;
  const end = parseInt(value);
  const speed = 30;
  const increment = end / 100;

  const update = setInterval(() => {
    count += increment;
    if (count >= end) {
      count = end;
      clearInterval(update);
    }
    num.textContent = Math.floor(count) + num.textContent.replace(/[0-9]/g, '');
  }, speed);
});


// Toggle between Week and Month Best Sellers
document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll(".toggle-btn");
  const weekSection = document.querySelector(".week-products");
  const monthSection = document.querySelector(".month-products");

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      buttons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      if (btn.dataset.target === "week") {
        weekSection.classList.remove("d-none");
        monthSection.classList.add("d-none");
      } else {
        monthSection.classList.remove("d-none");
        weekSection.classList.add("d-none");
      }
    });
  });
});


// Fade-in animation for New Arrivals section
document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".arrival-card");
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("fadeInUp");
      }
    });
  }, { threshold: 0.1 });

  cards.forEach(card => observer.observe(card));
});
