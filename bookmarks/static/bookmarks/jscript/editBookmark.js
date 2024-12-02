document.addEventListener("DOMContentLoaded", function () {
  setupEditButtonHandler();
  updateEditBookmarkImage();
  setupTagCleanup();
});

function setupEditButtonHandler() {
  const editButtons = document.querySelectorAll(".edit-bookmark-btn");

  editButtons.forEach((button) => {
    button.addEventListener("click", function (event) {
      event.stopPropagation();
      const bookmarkId = button.getAttribute("data-id");
      const modal = document.getElementById(`editBookmarkModal${bookmarkId}`);
      const title = button.getAttribute("data-title").trim();
      const category = button.getAttribute("data-category");
      const description = button.getAttribute("data-description");
      const tags = button.getAttribute("data-tags");
      const url = button.getAttribute("data-url");

      modal.querySelector(`#bookmark-title-${bookmarkId}`).value = title;
      modal.querySelector(`#bookmark-category-${bookmarkId}`).value = category;
      modal.querySelector(`#bookmark-description-${bookmarkId}`).value = description;
      modal.querySelector(`#bookmark-tags-${bookmarkId}`).value = tags;
      modal.querySelector(`#bookmark-url-${bookmarkId}`).value = url;
      modal.querySelector("form").action = `/bookmark/${bookmarkId}/edit/?next=${window.location.pathname}`;
    });
  });
}

function updateEditBookmarkImage() {
  document.querySelectorAll(".modal").forEach(function (modal) {
    const modalId = modal.id.split("editBookmarkModal")[1];
    const previewImage = document.getElementById(`bookmark-image-preview-${modalId}`);

    if (!previewImage) {
      return;
    }

    let originalImageSrc = previewImage.src;

    const fileInput = modal.querySelector('input[type="file"]');
    if (fileInput) {
      fileInput.addEventListener("change", function (event) {
        if (fileInput.files && fileInput.files[0]) {
          const reader = new FileReader();
          reader.onload = function (e) {
            previewImage.src = e.target.result;
          };
          reader.readAsDataURL(fileInput.files[0]);
        }
      });
    }

    modal.addEventListener("hide.bs.modal", function () {
      previewImage.src = originalImageSrc;
    });

    modal.addEventListener("show.bs.modal", function () {
      originalImageSrc = previewImage.src;
    });
  });
}

function setupTagCleanup() {
  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", function () {
      const tagsInput = form.querySelector("input[id^='bookmark-tags']");
      if (tagsInput) {
        cleanUpTags(tagsInput);
      }
    });
  });
}

function cleanUpTags(tagsInput) {
  let tags = tagsInput.value
    .split(",")
    .map((tag) => tag.trim())
    .filter((tag) => tag.length > 0);

  // If no tags are left, ensure the input is empty
  if (tags.length === 0) {
    tagsInput.value = "";
  } else {
    tagsInput.value = tags.join(", ");
  }
}