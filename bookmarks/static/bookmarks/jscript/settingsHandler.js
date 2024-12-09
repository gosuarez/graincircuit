document.addEventListener("DOMContentLoaded", function () {
  const emailForm = document.querySelector("form[action*='change_email']");
  const currentEmailInput = document.getElementById("current-email");
  const newEmailInput = document.getElementById("email");

  const passwordForm = document.getElementById("passwordForm");
  const deleteAccountForm = document.getElementById("deleteAccountForm");
  const deleteAccountFlashMessages = document.getElementById(
    "delete-account-flash-messages"
  );

  // Handle Email Update
  if (emailForm) {
    emailForm.addEventListener("submit", function (e) {
      e.preventDefault(); // Prevent the default form submission

      const formData = new FormData(emailForm);
      const csrfToken = document.querySelector(
        'input[name="csrfmiddlewaretoken"]'
      ).value;

      fetch(emailForm.action, {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": csrfToken,
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
          displayFlashMessage(
            data.success ? "success" : "danger",
            data.message
          );

          if (data.success) {
            // Update the current email field with the new email
            currentEmailInput.value = data.email;
          }
        })
        .catch((error) => {
          console.error("Error:", error.message);
          displayFlashMessage(
            "danger",
            error.message || "An unexpected error occurred."
          );
        })
        .finally(() => {
          // Clear the new email input field regardless of success or error
          newEmailInput.value = "";
        });
    });
  }

  // Handle Password Update
  if (passwordForm) {
    passwordForm.addEventListener("submit", function (e) {
      e.preventDefault(); // Prevent the default form submission

      const formData = new FormData(passwordForm);
      const csrfToken = document.querySelector(
        'input[name="csrfmiddlewaretoken"]'
      ).value;

      fetch(passwordForm.action, {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": csrfToken,
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
          displayFlashMessage(
            data.success ? "success" : "danger",
            data.message
          );

          if (data.success) {
            // Reset the password fields on success
            passwordForm.reset();
          }
        })
        .catch((error) => {
          console.error("Error:", error.message);
          displayFlashMessage(
            "danger",
            error.message || "An unexpected error occurred."
          );
        })
        .finally(() => {
          // Clear all password input fields regardless of success or error
          passwordForm.reset();
        });
    });
  }

  // Handle Account Deletion
  if (deleteAccountForm) {
    deleteAccountForm.addEventListener("submit", function (e) {
      e.preventDefault(); // Prevent the default form submission

      const formData = new FormData(deleteAccountForm);
      const csrfToken = document.querySelector(
        'input[name="csrfmiddlewaretoken"]'
      ).value;

      fetch(deleteAccountForm.action, {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": csrfToken,
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
            // Redirect the user to login after successful account deletion
            setTimeout(() => {
              window.location.href = data.redirect_url;
            }, 2000);
          } else {
            // Display error message inside the modal
            if (deleteAccountFlashMessages) {
              deleteAccountFlashMessages.innerHTML = ""; // Clear existing messages
              displayFlashMessage(
                data.success ? "success" : "danger",
                data.message,
                deleteAccountFlashMessages
              );
            }
          }
        })
        .catch((error) => {
          console.error("Error:", error.message);

          if (deleteAccountFlashMessages) {
            deleteAccountFlashMessages.innerHTML = ""; // Clear existing messages
            displayFlashMessage(
              "danger",
              error.message || "An unexpected error occurred.",
              deleteAccountFlashMessages
            );
          }
        });
    });
  }
});
