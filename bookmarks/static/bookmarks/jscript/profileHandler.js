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
            displayMessage("success", "Profile image updated successfully.");
          }
        })
        .catch((error) => {
          console.error("Error:", error.message);
          displayMessage("danger", error.message);
        });
    });
  }

  // Handle Username Update
  var usernameForm = document.getElementById("usernameForm");

  if (usernameForm) {
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
            const sidebarUsername = document.querySelector(
              ".sidebar .dropdown .text-none"
            );
            if (sidebarUsername) {
              sidebarUsername.textContent = formData.get("username");
            }

            displayMessage("success", data.message);
          }
        })
        .catch((error) => {
          console.error("Error:", error.message);
          displayMessage("danger", error.message);
        });
    });
  }

  // Flash Message Display Function
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
