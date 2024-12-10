document.addEventListener("DOMContentLoaded", function () {
  // Handle Profile Image Update
  var profileImageInput = document.getElementById("profile_image");
  var profileImageForm = document.getElementById("profileImageForm");

  if (profileImageInput && profileImageForm) {
    var formActionUrl = profileImageForm.dataset.url;

    profileImageInput.addEventListener("change", function () {
      var formData = new FormData(profileImageForm);

      fetch(formActionUrl, {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": getCsrfToken(),
        },
      })
        .then((response) =>
          response.json().then((data) => {
            if (!response.ok) {
              throw new Error(data.message || "An error occurred.");
            }
            return data;
          })
        )
        .then((data) => {
          if (data.success) {
            document.getElementById("profile-page-image").src = data.image_url;
            document.querySelector(".dropdown img.rounded-circle").src =
              data.image_url;
            clearFlashMessages(); // Clear existing messages
            displayFlashMessage(
              "success",
              "Profile image updated successfully."
            );
          }
        })
        .catch((error) => {
          console.error("Error:", error.message);
          clearFlashMessages(); // Clear existing messages
          displayFlashMessage("danger", error.message);
        })
        .finally(() => {
          // Clear the file input to allow the same file to trigger the change event again
          profileImageInput.value = "";
        });
    });
  }

  // Handle Username Update
  var usernameForm = document.getElementById("usernameForm");

  if (usernameForm) {
    const originalUsername = document.getElementById("username").value;

    usernameForm.addEventListener("submit", function (e) {
      e.preventDefault(); // Prevent default form submission

      var formData = new FormData(usernameForm);
      var formActionUrl = usernameForm.action;

      fetch(formActionUrl, {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": getCsrfToken(),
        },
      })
        .then((response) =>
          response.json().then((data) => {
            if (!response.ok) {
              throw new Error(data.message || "An error occurred.");
            }
            return data;
          })
        )
        .then((data) => {
          if (data.success) {
            // Update sidebar username
            const sidebarUsername = document.querySelector(
              ".sidebar .dropdown .text-none"
            );
            if (sidebarUsername) {
              sidebarUsername.textContent = formData.get("username");
            }

            clearFlashMessages(); // Clear existing messages
            displayFlashMessage("success", data.message);
          }
        })
        .catch((error) => {
          console.error("Error:", error.message);

          // Reset the username input field to the original value
          document.getElementById("username").value = originalUsername;

          clearFlashMessages(); // Clear existing messages
          displayFlashMessage("danger", error.message);
        });
    });
  }
});
