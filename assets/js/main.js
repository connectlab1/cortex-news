document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    if (!searchInput) return;

    const postItems = document.querySelectorAll(".post-item");

    searchInput.addEventListener("input", function (e) {
        const searchTerm = e.target.value.toLowerCase().trim();

        postItems.forEach(function (item) {
            const titleElement = item.querySelector(".post-title");
            const excerptElement = item.querySelector(".post-excerpt");

            const titleText = titleElement ? titleElement.textContent.toLowerCase() : "";
            const excerptText = excerptElement ? excerptElement.textContent.toLowerCase() : "";

            if (titleText.includes(searchTerm) || excerptText.includes(searchTerm)) {
                item.style.display = "";
            } else {
                item.style.display = "none";
            }
        });
    });
});
