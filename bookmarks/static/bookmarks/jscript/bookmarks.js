document.addEventListener("DOMContentLoaded", function () {
  ("use strict");
  addTooltips();
  window.addEventListener("resize", handleResize);
  setupCardClickHandler();
});

function addTooltips() {
  const navItems = document.querySelectorAll(".nav-item");
  const cardBtns = document.querySelectorAll(
    ".card-btns [data-bs-tooltip='tooltip']"
  );

  const isMobileOrTablet = /Mobi|Android|iPad|iPhone/i.test(
    navigator.userAgent
  );

  if (isMobileOrTablet) {
    // Remove tooltips on mobile devices
    removeTooltips(navItems);
    removeTooltips(cardBtns);
  } else {
    // Add tooltips for PC
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

        // Clean up existing tooltip instances
        if (bootstrap.Tooltip.getInstance(item)) {
          bootstrap.Tooltip.getInstance(item).dispose();
        }
      }
    });

    // Reinitialize tooltips
    initilizeTooltips();
  }
}

function removeTooltips(elements) {
  elements.forEach((item) => {
    item.removeAttribute("data-bs-tooltip");
    item.removeAttribute("data-bs-placement");
    item.removeAttribute("data-bs-original-title");

    // Clean up existing tooltip instances
    if (bootstrap.Tooltip.getInstance(item)) {
      bootstrap.Tooltip.getInstance(item).dispose();
    }
  });
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

function setupCardClickHandler() {
  const container = document.querySelector(".container-fluid");
  if (!container) return;

  container.addEventListener("click", handleCardClick);
}

function handleCardClick(event) {
  if (event.target.closest("a") || event.target.closest("button")) {
    return; 
  }

  const card = event.target.closest(".bookmark-card");

  if (card) {
    navigateToUrl(card.getAttribute("data-url"));
  }
}

function navigateToUrl(url) {
  window.open(url, '_blank');
}

function getCsrfToken() {
  const csrfTokenElement = document.querySelector('input[name="csrfmiddlewaretoken"]');
  return csrfTokenElement ? csrfTokenElement.value : null;
}


