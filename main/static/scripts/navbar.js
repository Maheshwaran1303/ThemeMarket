// navbar.js
window.addEventListener("scroll", function() {
  const navbar = document.querySelector(".navbar-fixed");
  if (window.scrollY > 10) {
    navbar.classList.add("scrolled");
  } else {
    navbar.classList.remove("scrolled");
  }
});

// Toggle Modal Visibility
function openAuthModal() {
  document.getElementById("authModal").style.display = "flex";
}

function closeAuthModal() {
  document.getElementById("authModal").style.display = "none";
}

// Switch Between Register & Login
document.addEventListener("DOMContentLoaded", () => {
  const switchToLogin = document.getElementById("switchToLogin");
  const switchToRegister = document.getElementById("switchToRegister");

  if (switchToLogin)
    switchToLogin.addEventListener("click", () => {
      fetch("/login/") // optional if dynamically loaded
    });

  if (switchToRegister)
    switchToRegister.addEventListener("click", () => {
      fetch("/register/")
    });
});



// Mega menu hover functionality
document.querySelectorAll('.mega-dropdown').forEach((item) => {
  item.addEventListener('mouseenter', () => {
    const menu = item.querySelector('.mega-menu');
    menu.classList.add('show');
  });
  item.addEventListener('mouseleave', () => {
    const menu = item.querySelector('.mega-menu');
    menu.classList.remove('show');
  });
});
