document.addEventListener("DOMContentLoaded", () => {
  // ==========================================
  // 1. Botão "Copiar" para Blocos de Código
  // ==========================================
  const codeBlocks = document.querySelectorAll("pre > code");

  codeBlocks.forEach((codeBlock) => {
    const pre = codeBlock.parentNode;

    // Evita duplicar o botão caso o script execute mais de uma vez
    if (pre.querySelector(".copy-code-btn")) return;

    const button = document.createElement("button");
    button.className = "copy-code-btn";
    button.type = "button";
    button.innerText = "Copiar";
    button.setAttribute("aria-label", "Copiar código para a área de transferência");

    button.addEventListener("click", () => {
      navigator.clipboard.writeText(codeBlock.innerText).then(() => {
        button.innerText = "Copiado!";
        button.classList.add("copied");

        setTimeout(() => {
          button.innerText = "Copiar";
          button.classList.remove("copied");
        }, 2000);
      }).catch((err) => {
        console.error("Erro ao copiar código: ", err);
        button.innerText = "Erro";
        setTimeout(() => {
          button.innerText = "Copiar";
        }, 2000);
      });
    });

    pre.style.position = "relative";
    pre.appendChild(button);
  });

  // ==========================================
  // 2. Toggle do Menu Mobile
  // ==========================================
  const menuToggle = document.querySelector(".menu-toggle");
  const navLinks = document.querySelector(".nav-links");

  if (menuToggle && navLinks) {
    menuToggle.addEventListener("click", () => {
      navLinks.classList.toggle("active");
      menuToggle.classList.toggle("active");
    });
  }
});
