document.addEventListener("DOMContentLoaded", function () {
  const colorBoxes = document.querySelectorAll(".color-selection");
  const radioInputs = document.querySelectorAll(".color-radio");
  const container = document.querySelector(".container[data-default-color]");
  const defaultColor = container
    ? container.getAttribute("data-default-color")
    : "#1E90FF"; // Fallback to the hardcoded color if not found

  let isAnyColorChecked = false;

  // Check if any radio input is checked
  radioInputs.forEach(function (input) {
    if (input.checked) {
      isAnyColorChecked = true;
      const associatedColorBox = input.nextElementSibling;
      associatedColorBox.classList.add("selected"); 
    }
  });

  // If no color is checked, select the default color
  if (!isAnyColorChecked) {
    const defaultColorInput = document.querySelector(
      `input[value="${defaultColor}"]`
    );
    if (defaultColorInput) {
      defaultColorInput.checked = true; 
      defaultColorInput.nextElementSibling.classList.add("selected"); 
    }
  }


  colorBoxes.forEach(function (box) {
    box.addEventListener("click", function () {
      colorBoxes.forEach((b) => b.classList.remove("selected"));

      this.classList.add("selected");

      const radioInput = this.previousElementSibling;
      radioInput.checked = true; 
    });
  });
});
