function filterBookmarks() {
  const searchInput = document.getElementById("searchBar").value.toLowerCase();
  const bookmarks = document.querySelectorAll(".bookmark-card");

  bookmarks.forEach((bookmark) => {
    const title = bookmark.getAttribute("data-title").toLowerCase();
    const category = bookmark.getAttribute("data-category").toLowerCase();
    const tags = bookmark.getAttribute("data-tags").toLowerCase();

    if (
      title.includes(searchInput) ||
      category.includes(searchInput) ||
      tags.includes(searchInput)
    ) {
      bookmark.style.display = "block";
    } else {
      bookmark.style.display = "none";
    }
  });
}

function filterCategories() {
  const searchInput = document.getElementById("searchBar").value.toLowerCase();
  const categories = document.querySelectorAll(".category-card"); 

  categories.forEach((category) => {
    const categoryName = category.textContent.toLowerCase();

    if (categoryName.includes(searchInput)) {
      category.style.display = "block";
    } else {
      category.style.display = "none";
    }
  });
}

