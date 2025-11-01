// Toggle between grid and list view

// document.addEventListener("DOMContentLoaded", function () {
//   const gridBtn = document.getElementById("gridView");
//   const listBtn = document.getElementById("listView");
//   const container = document.getElementById("productsContainer");

//   gridBtn.addEventListener("click", () => {
//     container.classList.remove("list");
//     container.classList.add("grid");
//     gridBtn.classList.add("active");
//     listBtn.classList.remove("active");
//   });

//   listBtn.addEventListener("click", () => {
//     container.classList.remove("grid");
//     container.classList.add("list");
//     listBtn.classList.add("active");
//     gridBtn.classList.remove("active");
//   });
// });

document.addEventListener("DOMContentLoaded", function () {
  const filters = [
    "categoryFilter",
    "priceFilter",
    "ratingFilter",
    "featuresFilter",
    "compatibilityFilter",
    "sortSelect",
  ];
  filters.forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.addEventListener("change", updateProducts);
  });

  const gridBtn = document.getElementById("gridView");
  const listBtn = document.getElementById("listView");
  const container = document.getElementById("productsContainer");
  let currentView = "grid";

  gridBtn.addEventListener("click", () => {
    container.classList.remove("list");
    container.classList.add("grid");
    gridBtn.classList.add("active");
    listBtn.classList.remove("active");
  });

  listBtn.addEventListener("click", () => {
    container.classList.remove("grid");
    container.classList.add("list");
    listBtn.classList.add("active");
    gridBtn.classList.remove("active");
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

    fetch(`/themes/filter/?${params.toString()}`)
      .then((res) => res.json())
      .then((data) => {
        const ajaxDiv = document.getElementById("ajax-products");
        ajaxDiv.classList.add("loading");
        setTimeout(() => {
          ajaxDiv.innerHTML = data.html;
          ajaxDiv.classList.remove("loading");
        }, 200);
      });
  }
});
