document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const searchResults = document.getElementById("search-results");

    if (!searchInput || !searchResults) return;

    let postsData = [];

    // Obtém o URL base configurado no botão/input via data attribute ou assume a raiz
    const searchJsonUrl = searchInput.getAttribute("data-search-json") || "/search.json";

    // Carrega o índice JSON
    fetch(searchJsonUrl)
    .then(response => response.json())
    .then(data => {
        postsData = data;
    })
    .catch(err => console.error("Erro ao carregar índice de busca:", err));

    searchInput.addEventListener("input", function (e) {
        const query = e.target.value.toLowerCase().trim();
        searchResults.innerHTML = "";

        if (query.length < 2) {
            return;
        }

        const filtered = postsData.filter(post => {
            return post.title.toLowerCase().includes(query) ||
            post.content.toLowerCase().includes(query) ||
            post.category.toLowerCase().includes(query);
        });

        if (filtered.length === 0) {
            searchResults.innerHTML = `<p style="grid-column: 1/-1; text-align: center; color: var(--text-muted);">Nenhum artigo encontrado para "<strong>${query}</strong>".</p>`;
            return;
        }

        filtered.forEach(post => {
            const card = document.createElement("article");
            card.className = "post-card";
            card.innerHTML = `
            <div class="post-categories"><span class="category-badge">${post.category}</span></div>
            <h2 class="post-title"><a href="${post.url}">${post.title}</a></h2>
            <p class="post-date"><time>${post.date}</time></p>
            <a href="${post.url}" class="read-more">Ler artigo &rarr;</a>
            `;
            searchResults.appendChild(card);
        });
    });
});
