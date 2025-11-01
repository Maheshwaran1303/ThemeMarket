document.addEventListener("DOMContentLoaded", function () {
  const filters = [
    "categoryFilter",
    "priceFilter",
    "ratingFilter",
    "featuresFilter",
    "compatibilityFilter",
    "sortSelect",
  ];

  const gridBtn = document.getElementById("gridView");
  const listBtn = document.getElementById("listView");
  const ajaxDiv = document.getElementById("ajax-products");
  let currentView = "grid";

  // Toggle grid/list view
  function applyViewClasses() {
    const container = document.getElementById("productsContainer");
    if (!container) return;
    container.classList.remove("grid", "list");
    container.classList.add(currentView);
  }

  gridBtn.addEventListener("click", () => {
    currentView = "grid";
    gridBtn.classList.add("active");
    listBtn.classList.remove("active");
    applyViewClasses();
  });

  listBtn.addEventListener("click", () => {
    currentView = "list";
    listBtn.classList.add("active");
    gridBtn.classList.remove("active");
    applyViewClasses();
  });

  // Filter functionality
  filters.forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.addEventListener("change", updateProducts);
  });

  function updateProducts() {
    const params = new URLSearchParams({
      category: document.getElementById("categoryFilter").value,
      price: document.getElementById("priceFilter").value,
      rating: document.getElementById("ratingFilter").value,
      features: document.getElementById("featuresFilter").value,
      compatibility: document.getElementById("compatibilityFilter").value,
      sort: document.getElementById("sortSelect").value,
      view: currentView,
    });

    ajaxDiv.classList.add("loading");

    fetch(`/themes/filter/?${params.toString()}`)
      .then((res) => res.json())
      .then((data) => {
        ajaxDiv.innerHTML = data.html;
        ajaxDiv.classList.remove("loading");
        applyViewClasses();

        // If no products, ensure user sees clear message
        const container = document.getElementById("productsContainer");
        if (!container || !container.querySelector(".product-card")) {
          ajaxDiv.innerHTML = `
            <div class="no-results">
              <i class="bi bi-emoji-frown"></i>
              <h4>No products found</h4>
              <p>Try changing your filters or search keywords.</p>
            </div>
          `;
        }
      })
      .catch(() => ajaxDiv.classList.remove("loading"));
  }
});
