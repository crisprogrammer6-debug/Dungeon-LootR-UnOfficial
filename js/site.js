(function () {
  const site = window.SITE;
  if (!site) return;

  const file = (location.pathname.split("/").pop() || "index.html").toLowerCase() || "index.html";

  const nav = document.getElementById("site-nav");
  if (nav) {
    nav.innerHTML = site.nav
      .map((item) => {
        const hrefFile = (item.href.split("?")[0] || "").toLowerCase();
        const current =
          hrefFile === file ||
          (file === "" && item.id === "home") ||
          (item.id === "gamemodes" &&
            (file === "raids.html" || file === "challenges.html" || file === "raids-info.html"));
        return `<a href="${item.href}" ${current ? "aria-current=\"page\"" : ""}>${item.label}</a>`;
      })
      .join("");
  }

  const source = document.getElementById("source");
  if (source && !source.textContent.trim()) source.textContent = site.source;

  if (nav && !document.getElementById("site-search")) {
    const wrap = document.createElement("div");
    wrap.className = "site-search";
    wrap.id = "site-search";
    wrap.innerHTML =
      '<label class="site-search-label" for="site-search-input">Search</label>' +
      '<input id="site-search-input" type="search" placeholder="Search classes, items, maps, NPCs…" autocomplete="off" />' +
      '<div class="site-search-results" hidden></div>';
    nav.after(wrap);
  }
})();
