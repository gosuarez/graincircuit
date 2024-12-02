document.addEventListener("DOMContentLoaded", function () {
  setupCardClickHandler();
});

function setupCardClickHandler() {
  const container = document.querySelector(".container-fluid");
  if (!container) return; 
  
  container.addEventListener("click", handleCardClick);
}

function handleCardClick(event) {
  const card = event.target.closest(".bookmark-card");
  if (card) {
    navigateToUrl(card.getAttribute("data-url"));
  }
}

function navigateToUrl(url) {
  window.location.href = url;
}
