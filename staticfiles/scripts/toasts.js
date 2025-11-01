// Automatically remove toast messages after animation
document.addEventListener("DOMContentLoaded", () => {
  const toasts = document.querySelectorAll(".toast-message");
  toasts.forEach((toast) => {
    setTimeout(() => {
      toast.remove();
    }, 5000);
  });
});
