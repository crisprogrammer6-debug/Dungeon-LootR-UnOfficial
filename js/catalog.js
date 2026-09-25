(function () {
  const site = window.SITE;
  const catalog = window.INDEX_CATALOG || {};
  const tabs = document.getElementById("index-tabs");
  const panel = document.getElementById("index-panel");
  if (!site || !tabs || !panel) return;

  const GRID_TABS = {
    items: { back: "All items" },
    consumables: { back: "All consumables" },
    materials: { back: "All materials" },
  };

  const params = new URLSearchParams(location.search);
  let current = params.get("tab") || "items";
  if (current === "cosmetics") current = "consumables";
  let itemId = params.get("id") || "";

  function listFor(tab) {
    return catalog[tab] || [];
  }

  function hrefFor(tab, id) {
    const q = new URLSearchParams();
    q.set("tab", tab);
    if (id) q.set("id", id);
    return `roster.html?${q.toString()}`;
  }

  function setUrl() {
    history.replaceState(null, "", hrefFor(current, GRID_TABS[current] ? itemId : ""));
  }

  function tileHtml(tab, m) {
    return `<a class="material-tile" href="${hrefFor(tab, m.id)}" data-index-tab="${tab}" data-index-id="${m.id}" title="${m.name}">
            <img src="${m.icon}?v=20" alt="${m.name}" />
          </a>`;
  }

  function groupedList(list) {
    const groups = [];
    for (const m of list) {
      const section = m.group || "";
      const last = groups[groups.length - 1];
      if (!last || last.section !== section) groups.push({ section, items: [m] });
      else last.items.push(m);
    }
    return groups;
  }

  function renderGrid(tab, list) {
    const label = site.indexTabs.find((t) => t.id === tab)?.label || tab;
    if (!list.length) {
      panel.className = "empty-panel";
      panel.innerHTML = `<p class="empty-ledger">${label} — nothing listed yet.</p>`;
      return;
    }
    panel.className = "index-panel is-materials";
    const groups = groupedList(list);
    panel.innerHTML = `<div class="index-groups">${groups
      .map((g) => {
        const heading = g.section ? `<p class="index-group-label">${g.section}</p>` : "";
        return `<section class="index-group">${heading}<div class="material-grid">${g.items
          .map((m) => tileHtml(tab, m))
          .join("")}</div></section>`;
      })
      .join("")}</div>`;
  }

  function raritySlug(r) {
    return String(r || "").toLowerCase().replace(/\s+/g, "-");
  }

  function cardRule() {
    return `<div class="item-card-rule" aria-hidden="true"><span></span><i></i><span></span></div>`;
  }

  function renderInfo(tab, entry) {
    const back = GRID_TABS[tab]?.back || "Back";
    const slug = raritySlug(entry.rarity);
    const rarityAttr = slug ? ` data-rarity="${slug}"` : "";
    let inner;
    const obtainBlock = entry.obtain
      ? `${cardRule()}
        <h3 class="item-card-obtain-label">How to obtain:</h3>
        <p class="item-card-obtain">${entry.obtain}</p>`
      : "";
    if (entry.rarity && entry.blurb) {
      inner = `
        <h2 class="item-card-title">${entry.name}</h2>
        <div class="item-card-head">
          <p class="item-card-rarity"><span>Rarity:</span><strong>${entry.rarity}</strong></p>
          <div class="item-card-icon"><img src="${entry.icon}?v=20" alt="" /></div>
        </div>
        ${cardRule()}
        <p class="item-card-blurb">${entry.blurb}</p>
        ${obtainBlock}`;
    } else if (entry.info) {
      inner = `
        <h2 class="item-card-title">${entry.name}</h2>
        <div class="item-card-icon is-solo"><img src="${entry.icon}?v=20" alt="" /></div>
        ${cardRule()}
        <div class="item-card-legacy">${entry.info}</div>
        ${obtainBlock}`;
    } else {
      inner = `
        <h2 class="item-card-title">${entry.name}</h2>
        <div class="item-card-icon is-solo"><img src="${entry.icon}?v=20" alt="" /></div>
        ${obtainBlock || `${cardRule()}
        <p class="material-info-soon">Details coming soon.</p>`}`;
    }
    panel.className = `index-panel is-materials is-detail${slug ? ` rarity-${slug}` : ""}`;
    panel.innerHTML = `<p class="back-row"><a href="${hrefFor(tab)}" data-index-back>${back.replace(/^All /, "← All ")}</a></p>
      <article class="item-card${slug ? "" : " is-soon"}"${rarityAttr}>
        <span class="item-card-corner tl" aria-hidden="true"></span>
        <span class="item-card-corner tr" aria-hidden="true"></span>
        <span class="item-card-corner bl" aria-hidden="true"></span>
        <span class="item-card-corner br" aria-hidden="true"></span>
        ${inner}
      </article>`;
  }

  function render() {
    tabs.innerHTML = site.indexTabs
      .map(
        (tab) =>
          `<button class="chip" data-tab="${tab.id}" aria-pressed="${tab.id === current}">${tab.label}</button>`
      )
      .join("");
    const active = site.indexTabs.find((t) => t.id === current) || site.indexTabs[0];
    if (GRID_TABS[active.id]) {
      const list = listFor(active.id);
      const entry = itemId ? list.find((m) => m.id === itemId) : null;
      if (itemId && entry) {
        renderInfo(active.id, entry);
        return;
      }
      itemId = "";
      renderGrid(active.id, list);
      return;
    }
    panel.className = "empty-panel";
    panel.innerHTML = `<p class="empty-ledger">${active.label} — nothing listed yet.</p>`;
  }

  tabs.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-tab]");
    if (!btn) return;
    current = btn.dataset.tab;
    itemId = "";
    setUrl();
    render();
  });

  panel.addEventListener("click", (e) => {
    const back = e.target.closest("[data-index-back]");
    if (back) {
      e.preventDefault();
      itemId = "";
      setUrl();
      render();
      return;
    }
    const tile = e.target.closest("[data-index-id]");
    if (!tile) return;
    e.preventDefault();
    current = tile.dataset.indexTab || current;
    itemId = tile.dataset.indexId;
    setUrl();
    render();
    window.scrollTo(0, 0);
  });

  render();
})();
