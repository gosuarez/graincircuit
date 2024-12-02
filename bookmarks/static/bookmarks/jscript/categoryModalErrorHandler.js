document.addEventListener("DOMContentLoaded", function () {
  var errorMessageExists = document.querySelector(".alert-danger");
  var addCategoryModalElement = document.getElementById("addCategoryModal");
  var renameCategoryId = document.getElementById("rename_category_id");
  var renameCategoryModalElement = renameCategoryId
    ? document.getElementById("renameCategoryModal" + renameCategoryId.value)
    : null;

  if (errorMessageExists) {
    if (renameCategoryModalElement) {
      var renameCategoryModal = new bootstrap.Modal(renameCategoryModalElement);
      renameCategoryModal.show();
    } else if (addCategoryModalElement) {
      var addCategoryModal = new bootstrap.Modal(addCategoryModalElement);
      addCategoryModal.show();
    }
  }
});
