document.addEventListener("DOMContentLoaded", function () {
  addTooltips();
  window.addEventListener("resize", handleResize);
});

function addTooltips() {
  const navItems = document.querySelectorAll(".nav-item");

  navItems.forEach((item) => {
    const span = item.querySelector("span");
    const title = span ? span.textContent.trim() : "";

    if (window.innerWidth < 767 && title) {
      item.setAttribute("data-bs-tooltip", "tooltip");
      item.setAttribute("data-bs-placement", "right");
      item.setAttribute("data-bs-original-title", title);
    } else {
      item.removeAttribute("data-bs-tooltip");
      item.removeAttribute("data-bs-placement");
      item.removeAttribute("data-bs-original-title");

      if (bootstrap.Tooltip.getInstance(item)) {
        bootstrap.Tooltip.getInstance(item).dispose();
      }
    }
  });

  initilizeTooltips();
}

function initilizeTooltips() {
  document
    .querySelectorAll('[data-bs-tooltip="tooltip"]')
    .forEach((tooltipTriggerEl) => {
      new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function handleResize() {
  addTooltips();
}
