document.addEventListener("DOMContentLoaded", function () {
  var categoryList = document.getElementById("category-list");

 
  if (!categoryList) {
    return; 
  }

  var csrfToken = getCsrfToken();

  var sortable = new Sortable(categoryList, {
    animation: 150,
    handle: ".category-drag-handle",
    onEnd: function (evt) {
      var order = [];
      categoryList
        .querySelectorAll(".category-card")
        .forEach(function (card, index) {
          order.push({
            id: card.getAttribute("data-id"),
            position: index + 1,
          });
        });

      fetch("/update_category_order/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ order: order }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status) {
            console.log("Category order updated successfully");
          } else {
            console.error("Error updating category order:", data.message);
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },
  });
});
