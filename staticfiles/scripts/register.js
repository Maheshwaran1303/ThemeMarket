document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("authModal");
  const closeBtn = document.getElementById("closeModal");
  const personIcon = document.getElementById("personIcon");

  personIcon.addEventListener("click", (e) => {
    e.preventDefault();
    modal.style.display = "flex";
    document.body.style.overflow = "hidden";
  });

  closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
    document.body.style.overflow = "auto";
  });

  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
      document.body.style.overflow = "auto";
    }
  });
});
