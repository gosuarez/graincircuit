document.addEventListener("DOMContentLoaded", function () {
  var flashMessages = document.getElementById("flash-messages");
  var addBookmarkModal = new bootstrap.Modal(
    document.getElementById("addBookmarkModal")
  );

  if (flashMessages && flashMessages.children.length > 0) {
    addBookmarkModal.show();
  }

  document
    .getElementById("addBookmarkModal")
    .addEventListener("hidden.bs.modal", function () {
      if (flashMessages) {
        flashMessages.innerHTML = "";
      }
    });
});
