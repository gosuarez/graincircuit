document.addEventListener("DOMContentLoaded", function () {
  // Handle Profile Image Update
  const profileImageInput = document.getElementById("profile_image");
  const profileImageForm = document.getElementById("profileImageForm");

  if (profileImageInput && profileImageForm) {
    const formActionUrl = profileImageForm.dataset.url;

    profileImageInput.addEventListener("change", function () {
      const formData = new FormData(profileImageForm);

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
            displayFlashMessage(
              "success",
              "Profile image updated successfully."
            );
          }
        })
        .catch((error) => {
          console.error("Error:", error.message);
          displayFlashMessage("danger", error.message);
        });
    });
  }

  // Handle Username Update
  const usernameForm = document.getElementById("usernameForm");

  if (usernameForm) {
    const originalUsername = document.getElementById("username").value;

    usernameForm.addEventListener("submit", function (e) {
      e.preventDefault(); // Prevent default form submission

      const formData = new FormData(usernameForm);
      const formActionUrl = usernameForm.action;

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

            displayFlashMessage("success", data.message);
          }
        })
        .catch((error) => {
          console.error("Error:", error.message);

          // Reset the username input field to the original value
          document.getElementById("username").value = originalUsername;

          displayFlashMessage("danger", error.message);
        });
    });
  }
});
