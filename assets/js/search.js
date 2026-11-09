document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const searchResults = document.getElementById("search-results");

    if (!searchInput || !searchResults) {
        console.warn("Elementos de busca (search-input ou search-results) não encontrados na página.");
        return;
    }

    let postsData = [];
    let isLoaded = false;
    const searchJsonUrl = searchInput.getAttribute("data-search-json") || "/search.json";

    function normalizar(texto) {
        if (Array.isArray(texto)) {
            texto = texto.join(" ");
        }
        return (texto || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    }

    // Carrega o índice de posts gerado pelo Jekyll
    fetch(searchJsonUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status} - Certifique-se de que o ficheiro 'search.json' existe na raiz.`);
        }
        return response.json();
    })
    .then(data => {
        postsData = data;
        isLoaded = true;
    })
    .catch(err => {
        console.error("Erro ao carregar índice de busca:", err);
        searchResults.innerHTML = `<p style="font-size: 0.85rem; color: #ef4444; text-align: center; padding: 0.5rem;">Erro ao carregar dados de pesquisa.</p>`;
    });

    searchInput.addEventListener("input", function (e) {
        const queryBruta = e.target.value.trim();
        const query = normalizar(queryBruta);

        searchResults.innerHTML = "";

        if (query.length < 2) {
            return;
        }

        if (!isLoaded) {
            searchResults.innerHTML = `<p style="font-size: 0.85rem; color: var(--text-muted, #888); text-align: center; padding: 0.5rem;">A carregar índice, aguarde...</p>`;
            return;
        }

        const filtered = postsData.filter(post => {
            return normalizar(post.title).includes(query) ||
            normalizar(post.content).includes(query) ||
            normalizar(post.category).includes(query) ||
            normalizar(post.tags).includes(query);
        });

        if (filtered.length === 0) {
            searchResults.innerHTML = `<p style="font-size: 0.85rem; color: var(--text-muted, #888); text-align: center; padding: 0.5rem;">Nenhum resultado para "<strong>${queryBruta}</strong>".</p>`;
            return;
        }

        filtered.forEach(post => {
            const item = document.createElement("div");
            item.style.cssText = "padding: 0.5rem 0; border-bottom: 1px dashed var(--border-color, #333);";

            const categoriaFormatada = Array.isArray(post.category) ? post.category.join(", ") : (post.category || "");

            item.innerHTML = `
            <div style="font-size: 0.75rem; color: var(--accent, #38bdf8); margin-bottom: 0.2rem;">${categoriaFormatada}</div>
            <a href="${post.url}" style="font-size: 0.85rem; font-weight: 600; color: var(--text-main, #fff); text-decoration: none; display: block; line-height: 1.2;">${post.title}</a>
            <span style="font-size: 0.7rem; color: var(--text-muted, #aaa);">${post.date || ""}</span>
            `;
            searchResults.appendChild(item);
        });
    });
});
