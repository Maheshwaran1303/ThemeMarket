document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".qty-btn").forEach(button => {
    button.addEventListener("click", async (e) => {
      const parent = e.target.closest(".quantity-controls");
      const itemId = parent.getAttribute("data-item-id");
      const qtySpan = parent.querySelector(".qty");
      const action = e.target.classList.contains("increase") ? "increase" : "decrease";

      const response = await fetch("/cart/update/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": getCookie("csrftoken")
        },
        body: `item_id=${itemId}&action=${action}`
      });

      const data = await response.json();

      if (!data.error) {
        qtySpan.textContent = data.quantity;
        document.getElementById("cart-total").textContent = `US$ ${data.total.toFixed(2)}`;
        document.getElementById("cart-savings").textContent = `Total Saving $${data.savings.toFixed(2)}`;
        document.getElementById("cart-grand").textContent = `Grand Total $${data.grand_total.toFixed(2)}`;
      }
    });
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
