document.addEventListener("DOMContentLoaded", function () {
  const emailForm = document.querySelector("form[action*='change_email']");
  const currentEmailInput = document.getElementById("current-email");
  const newEmailInput = document.getElementById("email");

  const passwordForm = document.getElementById("passwordForm");
  const deleteAccountForm = document.getElementById("deleteAccountForm");
  const deleteAccountSpinner = document.getElementById(
    "delete-account-spinner"
  );
  const deleteAccountModal = document.getElementById("deleteAccountModal");
  const deleteAccountBootstrapModal = deleteAccountModal
    ? bootstrap.Modal.getInstance(deleteAccountModal) ||
      new bootstrap.Modal(deleteAccountModal)
    : null;

  // Handle Email Update
  if (emailForm) {
    emailForm.addEventListener("submit", function (e) {
      e.preventDefault(); // Prevent the default form submission

      const formData = new FormData(emailForm);
      const csrfToken = document.querySelector(
        'input[name="csrfmiddlewaretoken"]'
      ).value;

      clearFlashMessages(); // Clear existing messages

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

      clearFlashMessages(); // Clear existing messages

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

  // Handle Delete Account
  if (deleteAccountForm) {
    deleteAccountForm.addEventListener("submit", function (e) {
      e.preventDefault(); // Prevent default submission

      const formData = new FormData(deleteAccountForm);
      const csrfToken = document.querySelector(
        'input[name="csrfmiddlewaretoken"]'
      ).value;

      // Show the spinner and disable the delete button
      if (deleteAccountSpinner) {
        deleteAccountSpinner.classList.remove("d-none");
      }
      deleteAccountForm.querySelector("button[type='submit']").disabled = true;

      clearFlashMessages(); // Clear existing messages

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
            // Redirect immediately after showing the success message
            window.location.href = data.redirect_url;
          } else {
            displayFlashMessage("danger", data.message);

            // Explicitly close the modal on failure
            if (deleteAccountBootstrapModal) {
              deleteAccountBootstrapModal.hide();
            }
          }
        })
        .catch((error) => {
          console.error("Error:", error.message);
          displayFlashMessage(
            "danger",
            error.message || "An unexpected error occurred."
          );

          // Explicitly close the modal on error
          if (deleteAccountBootstrapModal) {
            deleteAccountBootstrapModal.hide();
          }
        })
        .finally(() => {
          // Hide the spinner and re-enable the delete button
          if (deleteAccountSpinner) {
            deleteAccountSpinner.classList.add("d-none");
          }
          deleteAccountForm.querySelector(
            "button[type='submit']"
          ).disabled = false;
        });
    });
  }
});
