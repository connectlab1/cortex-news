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
      const textToCopy = codeBlock.innerText;

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(textToCopy).then(() => {
          showSuccessState(button);
        }).catch((err) => {
          console.error("Erro ao copiar com Clipboard API: ", err);
          fallbackCopyText(textToCopy, button);
        });
      } else {
        fallbackCopyText(textToCopy, button);
      }
    });

    pre.style.position = "relative";
    pre.appendChild(button);
  });

  // Função auxiliar para sucesso na cópia
  function showSuccessState(button) {
    button.innerText = "Copiado!";
    button.classList.add("copied");

    setTimeout(() => {
      button.innerText = "Copiar";
      button.classList.remove("copied");
    }, 2000);
  }

  // Fallback legado para cópia (caso navigator.clipboard falhe)
  function fallbackCopyText(text, button) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";  // Evita rolagem da página
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      const successful = document.execCommand('copy');
      if (successful) {
        showSuccessState(button);
      } else {
        showErrorState(button);
      }
    } catch (err) {
      console.error("Erro no fallback de cópia: ", err);
      showErrorState(button);
    }

    document.body.removeChild(textArea);
  }

  function showErrorState(button) {
    button.innerText = "Erro";
    setTimeout(() => {
      button.innerText = "Copiar";
    }, 2000);
  }

  // ==========================================
  // 2. Toggle do Menu Mobile com Acessibilidade
  // ==========================================
  const menuToggle = document.querySelector(".menu-toggle");
  const navLinks = document.querySelector(".nav-links");

  if (menuToggle && navLinks) {
    menuToggle.addEventListener("click", () => {
      const isActive = navLinks.classList.toggle("active");
      menuToggle.classList.toggle("active");

      // Atualiza atributo de acessibilidade dinamicamente
      menuToggle.setAttribute("aria-expanded", isActive);
    });
  }

  // ==========================================
  // 3. Segurança em Links Externos Automáticos
  // ==========================================
  const postLinks = document.querySelectorAll(".post-content a, .post-excerpt a");
  const currentHost = window.location.hostname;

  postLinks.forEach((link) => {
    if (link.hostname && link.hostname !== currentHost) {
      link.setAttribute("target", "_blank");
      link.setAttribute("rel", "noopener noreferrer");
    }
  });
});
