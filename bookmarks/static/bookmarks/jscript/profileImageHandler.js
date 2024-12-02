document.addEventListener("DOMContentLoaded", function () {
  var profileImageInput = document.getElementById("profile_image");
  var profileImageForm = document.getElementById("profileImageForm");

  if (profileImageInput && profileImageForm) {
    var formActionUrl = profileImageForm.dataset.url; 
    var csrfToken = profileImageForm.dataset.csrfToken; 

    profileImageInput.addEventListener("change", function () {
      var formData = new FormData(profileImageForm);

      fetch(formActionUrl, {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": csrfToken,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            document.getElementById("profile-page-image").src = data.image_url;

            document.querySelector(".dropdown img.rounded-circle").src =
              data.image_url;

            displayMessage("success", "Profile image updated successfully.");
          } else {
         
            displayMessage("danger", "Failed to upload the image.");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
      
          displayMessage(
            "danger",
            "An error occurred while updating the profile image."
          );
        });
    });
  }

  function displayMessage(type, message) {
    const messagesDiv = document.querySelector(".flash-messages");
    const alertDiv = document.createElement("div");
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = "alert";
    alertDiv.innerHTML = `
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    messagesDiv.appendChild(alertDiv);
  }
});
