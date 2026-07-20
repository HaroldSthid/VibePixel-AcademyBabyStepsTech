(() => {
  const tree = [
    {
      key: "inicio",
      label: "Inicio",
      href: "index.html",
      before: "Nada: esta es la puerta de entrada.",
      after: "Seguís con Onboarding.",
    },
    {
      key: "onboarding",
      label: "Onboarding",
      href: "onboarding.html",
      before: "Primero pasás por Inicio.",
      after: "Después seguís con la vista de plataformas o con Desafío RGB.",
    },
    {
      key: "platforms",
      label: "Plataformas",
      href: "platforms.html",
      before: "Antes necesitás Onboarding.",
      after: "Después elegís GitHub, Colab o CodePen.",
      note: "Vista de contexto: ayuda a entender cada interfaz sin entrar todavía en el video final.",
    },
    {
      key: "rgb",
      label: "Desafío RGB",
      href: "artifacts/rgb-discovery/rgb-discovery.html",
      before: "Antes necesitás Onboarding.",
      after: "Luego seguís con Colab.",
    },
    {
      key: "colab",
      label: "Colab actual",
      href: "colab-onboarding.html",
      before: "Antes necesitás el Desafío RGB.",
      after: "Después seguís con CodePen.",
      note: "El pipeline de avatar y los datos de ejemplo ya están disponibles. La guía paso a paso de Colab RGB ya está publicada.",
    },
    {
      key: "codepen",
      label: "CodePen",
      href: "codepen-onboarding.html",
      before: "Antes necesitás Colab.",
      after: "Después seguís con GitHub sin miedo.",
    },
    {
      key: "github",
      label: "GitHub sin miedo",
      href: "github-onboarding.html",
      before: "Antes necesitás CodePen.",
      after: "Después seguís con Entrega Top 10.",
    },
    {
      key: "submissions",
      label: "Entrega Top 10",
      href: "submissions.html",
      before: "Antes necesitás GitHub sin miedo.",
      after: "Después cerrás el recorrido y compartís la evidencia.",
    },
    {
      key: "top10",
      label: "Top 10",
      href: "top10.html",
      before: "Antes necesitás haber pasado por Entrega Top 10.",
      after: "Después queda la referencia para celebraciones y reconocimiento.",
      note: "Publicación manual: solo muestra entregas revisadas y seleccionadas.",
    },
  ];

  const extras = [
    { label: "Mapa del sitio", href: "sitemap.html" },
    { label: "Plataformas", href: "platforms.html" },
    { label: "Guía en GitHub", href: "https://github.com/HaroldSthid/VibePixel-AcademyBabyStepsTech" },
    { label: "Referencia Markdown", href: "https://github.com/HaroldSthid/VibePixel-AcademyBabyStepsTech/tree/main/docs" },
  ];

  const body = document.body;
  if (!body || body.querySelector(".site-map")) {
    return;
  }

  const root = normalizeRoot(body.dataset.siteRoot || "");
  const currentKey = body.dataset.siteKey || inferKeyFromPath(window.location.pathname);
  const currentPage = tree.find((item) => item.key === currentKey) || {
    label: body.dataset.siteLabel || document.title.replace(/\s*\|\s*.*$/, "").trim() || "Mapa del sitio",
    before: "Ubicate antes de seguir.",
    after: "Usá el mapa para elegir el próximo paso.",
  };

  const siteMap = document.createElement("div");
  siteMap.className = "site-map";
  siteMap.dataset.open = "false";
  siteMap.innerHTML = `
    <button type="button" class="site-map__toggle" aria-controls="site-map-drawer" aria-expanded="false" aria-label="Abrir mapa lateral de aprendizaje">Mapa</button>
    <div class="site-map__overlay" hidden></div>
    <aside id="site-map-drawer" class="site-map__drawer" aria-hidden="true" aria-label="Mapa lateral de aprendizaje">
      <div class="site-map__panel" role="document">
        <header class="site-map__header">
          <div>
            <p class="site-map__eyebrow">Mapa lateral</p>
            <h2 class="site-map__title">Ruta de aprendizaje</h2>
          </div>
          <button type="button" class="site-map__close" aria-label="Cerrar mapa lateral de aprendizaje">Cerrar</button>
        </header>

        <section class="site-map__current" aria-label="Contexto actual">
          <p class="site-map__current-label">Estás acá</p>
          <h3 class="site-map__current-name">${escapeHtml(currentPage.label)}</h3>
          <p class="site-map__context"><strong>Antes necesitás…</strong> ${escapeHtml(currentPage.before || "Nada.")}</p>
          <p class="site-map__context"><strong>Después seguís con…</strong> ${escapeHtml(currentPage.after || "El siguiente paso de la ruta.")}</p>
        </section>

        <nav class="site-map__tree" aria-label="Ruta principal">
          <ul class="site-map__tree-list">
            ${tree.map(renderTreeItem).join("")}
          </ul>
        </nav>

        <section class="site-map__secondary" aria-label="Apoyos secundarios">
          <h3 class="site-map__secondary-title">Apoyos secundarios</h3>
          <div class="site-map__secondary-links">
            ${extras
              .map((item) => `<a href="${escapeAttribute(joinRoot(root, item.href))}">${escapeHtml(item.label)}</a>`)
              .join("")}
          </div>
        </section>
      </div>
    </aside>
  `;

  body.appendChild(siteMap);

  const toggle = siteMap.querySelector(".site-map__toggle");
  const drawer = siteMap.querySelector(".site-map__drawer");
  const overlay = siteMap.querySelector(".site-map__overlay");
  const closeButton = siteMap.querySelector(".site-map__close");
  const focusTarget = closeButton;
  const supportsInert = "inert" in drawer;
  const managedTabindex = new Map();
  drawer.tabIndex = -1;
  const focusableSelector = [
    'a[href]',
    'button:not([disabled])',
    'input:not([disabled])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])',
  ].join(', ');

  setDrawerState(false);

  const open = () => {
    siteMap.dataset.open = "true";
    overlay.hidden = false;
    toggle.setAttribute("aria-expanded", "true");
    toggle.setAttribute("aria-label", "Cerrar mapa lateral de aprendizaje");
    setDrawerState(true);
    window.setTimeout(() => {
      (focusTarget || drawer).focus();
    }, 0);
  };

  const close = () => {
    siteMap.dataset.open = "false";
    overlay.hidden = true;
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Abrir mapa lateral de aprendizaje");
    setDrawerState(false);
    toggle.focus();
  };

  toggle.addEventListener("click", () => {
    if (siteMap.dataset.open === "true") {
      close();
    } else {
      open();
    }
  });

  closeButton.addEventListener("click", close);
  overlay.addEventListener("click", close);

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && siteMap.dataset.open === "true") {
      close();
      return;
    }

    if (event.key !== "Tab" || siteMap.dataset.open !== "true") {
      return;
    }

    const focusables = getFocusableElements(drawer);
    if (!drawer.contains(document.activeElement)) {
      event.preventDefault();
      (focusables[0] || focusTarget || drawer).focus();
      return;
    }

    if (focusables.length === 0) {
      event.preventDefault();
      drawer.focus();
      return;
    }

    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    const active = document.activeElement;

    if (event.shiftKey && active === first) {
      event.preventDefault();
      last.focus();
      return;
    }

    if (!event.shiftKey && active === last) {
      event.preventDefault();
      first.focus();
    }
  });

  function renderTreeItem(item) {
    const isCurrent = item.key === currentKey;
    return `
      <li class="site-map__tree-item${isCurrent ? " site-map__tree-item--current" : ""}">
        <div class="site-map__tree-main">
          <a class="site-map__link" href="${escapeAttribute(joinRoot(root, item.href))}">
            <span>${escapeHtml(item.label)}</span>
            ${isCurrent ? '<span class="site-map__badge site-map__badge--current">Estás acá</span>' : ""}
          </a>
          <details class="site-map__details">
            <summary>Ver detalle</summary>
            <div class="site-map__details-body">
              <p><strong>Antes necesitás…</strong> ${escapeHtml(item.before)}</p>
              <p><strong>Después seguís con…</strong> ${escapeHtml(item.after)}</p>
              ${item.note ? `<p class="site-map__details-note">${escapeHtml(item.note)}</p>` : ""}
            </div>
          </details>
        </div>
      </li>
    `;
  }

  function setDrawerState(isOpen) {
    drawer.setAttribute("aria-hidden", isOpen ? "false" : "true");

    if (supportsInert) {
      drawer.inert = !isOpen;
      return;
    }

    if (isOpen) {
      for (const element of Array.from(managedTabindex.keys())) {
        restoreTabIndex(element);
      }

      return;
    }

    for (const element of getFocusableElements(drawer)) {
      lockTabIndex(element);
    }
  }

  function lockTabIndex(element) {
    if (managedTabindex.has(element)) {
      return;
    }

    managedTabindex.set(element, element.getAttribute("tabindex"));
    element.setAttribute("tabindex", "-1");
  }

  function restoreTabIndex(element) {
    if (!managedTabindex.has(element)) {
      return;
    }

    const previousTabIndex = managedTabindex.get(element);
    managedTabindex.delete(element);

    if (previousTabIndex === null) {
      element.removeAttribute("tabindex");
      return;
    }

    element.setAttribute("tabindex", previousTabIndex);
  }

  function normalizeRoot(value) {
    if (!value) {
      return "";
    }

    return value.endsWith("/") ? value : `${value}/`;
  }

  function joinRoot(root, href) {
    if (/^(?:[a-z]+:)?\/\//i.test(href)) {
      return href;
    }

    return `${root}${href}`;
  }

  function inferKeyFromPath(pathname) {
    if (pathname.endsWith("/artifacts/rgb-discovery/rgb-discovery.html")) {
      return "rgb";
    }

    if (pathname.endsWith("/index.html") || pathname === "/" || pathname === "") {
      return "inicio";
    }

    const file = pathname.split("/").filter(Boolean).pop() || "";
    switch (file) {
      case "onboarding.html":
        return "onboarding";
      case "platforms.html":
        return "platforms";
      case "sitemap.html":
        return "sitemap";
      case "colab-onboarding.html":
        return "colab";
      case "codepen-onboarding.html":
        return "codepen";
      case "github-onboarding.html":
        return "github";
      case "submissions.html":
        return "submissions";
      case "top10.html":
        return "top10";
      default:
        return "";
    }
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function escapeAttribute(value) {
    return escapeHtml(value);
  }

  function getFocusableElements(container) {
    return Array.from(container.querySelectorAll(focusableSelector)).filter((element) => {
      const style = window.getComputedStyle(element);
      return style.display !== "none" && style.visibility !== "hidden";
    });
  }
})();
