document.addEventListener("DOMContentLoaded", function () {
  const csrfToken = getCsrfToken();
  const bookmarkList = document.getElementById("bookmark-list");

  if (!bookmarkList) return; 

  new Sortable(bookmarkList, {
    handle: ".bookmark-drag-handle",
    onEnd: function () {
      const uniqueDataIds = [
        ...new Set(
          Array.from(document.querySelectorAll(".bookmark-card")).map((card) =>
            card.getAttribute("data-id")
          )
        ),
      ];

      const parsedOrder = uniqueDataIds.map(Number); 

      fetch("/update_bookmark_order/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ order: parsedOrder }),
      })
        .then((response) => {
          if (!response.ok)
            throw new Error(`HTTP error! status: ${response.status}`);
          return response.json();
        })
        .then((data) => {
          console.log("Bookmark order updated successfully");
        })
        .catch((error) => {
          console.error("Error updating bookmark order:", error);
        });
    },
  });
});
