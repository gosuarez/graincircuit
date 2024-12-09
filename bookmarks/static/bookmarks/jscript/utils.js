/**
 * Utility function to display messages in a specified container.
 * @param {string} type - Type of message (e.g., 'success', 'danger').
 * @param {string} message - The message to display.
 * @param {HTMLElement} targetContainer - The container where the message should be displayed.
 */
function displayFlashMessage(type, message, targetContainer = null) {
  // Use the provided container or fall back to the global flash-messages container
  const container =
    targetContainer || document.querySelector(".flash-messages");

  if (!container) {
    console.error("Flash messages container not found.");
    return;
  }

  // Clear existing messages
  clearFlashMessages(container);

  // Create and append new message
  const alertDiv = document.createElement("div");
  alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
  alertDiv.role = "alert";
  alertDiv.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;
  container.appendChild(alertDiv);
}

/**
 * Utility function to clear all existing flash messages from a specified container.
 * @param {HTMLElement} targetContainer - The container from which messages should be cleared.
 */
function clearFlashMessages(targetContainer = null) {
  const container =
    targetContainer || document.querySelector(".flash-messages");

  if (!container) {
    console.error("Flash messages container not found.");
    return;
  }

  container.innerHTML = ""; // Clear all child elements
}
