(function () {
  const data = window.LOOTR;
  const board = document.getElementById("board");
  const search = document.getElementById("search");
  const filters = document.getElementById("filters");
  const legend = document.getElementById("legend");
  const podiums = document.getElementById("podiums");
  const tierRank = Object.fromEntries(data.TIERS.map((t, i) => [t.id, i]));

  let rarityFilter = "all";

  const SHIELDS = new Set(["aegis", "alacrity", "fulmin"]);
  const listOrder = Object.fromEntries(data.CLASSES.map((c, i) => [c.name, i]));

  function icon(archetype, extraClass = "") {
    const src = data.ARCHETYPES[archetype]?.icon;
    if (!src) return "";
    const cls = [extraClass, SHIELDS.has(archetype) ? "is-shield" : ""].filter(Boolean).join(" ");
    return `<img class="${cls}" src="${src}" alt="">`;
  }

  function renderLegend() {
    legend.innerHTML = Object.entries(data.RARITIES)
      .map(([, r]) => `<span><i style="background:${r.hex};color:${r.hex}"></i>${r.label}</span>`)
      .join("");
  }

  function renderFilters() {
    const all = `<button class="chip" data-rarity="all" aria-pressed="true">All</button>`;
    const rest = Object.entries(data.RARITIES)
      .map(([id, r]) => `<button class="chip" data-rarity="${id}" aria-pressed="false">${r.label}</button>`)
      .join("");
    filters.innerHTML = all + rest;
  }

  function matches(cls, q) {
    if (rarityFilter !== "all" && cls.rarity !== rarityFilter) return false;
    if (!q) return true;
    return `${cls.name} ${cls.archetype} ${cls.rarity}`.toLowerCase().includes(q);
  }

  function classHref(cls) {
    const id = String(cls.name || "")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "");
    return `classes.html?id=${id}`;
  }

  function cardHTML(cls) {
    const rarity = data.RARITIES[cls.rarity];
    const arch = data.ARCHETYPES[cls.archetype];
    const neu = cls.isNew ? `<span class="tag-new">NEW</span>` : "";
    return `<a class="card${cls.isNew ? " is-new" : ""}" href="${classHref(cls)}" style="--rarity:${rarity?.hex || "#888"}">
      ${neu}
      <div>
        <div class="name">${cls.name}</div>
        <div class="sub">${arch?.label || cls.archetype} · ${rarity?.label || cls.rarity}</div>
      </div>
      <div class="glyph">${icon(cls.archetype)}</div>
    </a>`;
  }

  function renderBoard() {
    const q = (search.value || "").trim().toLowerCase();
    board.innerHTML = data.TIERS.map((tier) => {
      const classes = data.CLASSES.filter((c) => c.tier === tier.id && matches(c, q));
      const cards = classes.length
        ? classes.map(cardHTML).join("")
        : `<div class="empty">No classes in this rank for the current filter.</div>`;
      return `<section class="row" data-tier="${tier.id}">
        <div class="rank"><span class="rank-label">${tier.label}</span></div>
        <div class="grid">${cards}</div>
      </section>`;
    }).join("");
  }

  function renderPodiums() {
    const q = (search.value || "").trim().toLowerCase();
    const places = [
      { key: "silver", medal: "II" },
      { key: "gold", medal: "I" },
      { key: "bronze", medal: "III" },
    ];

    const marks = data.MARKS || [];
    podiums.innerHTML = marks
      .map((mark) => {
        const set = new Set(mark.archetypes);
        const ranked = data.CLASSES.filter((c) => set.has(c.archetype) && matches(c, q)).sort(
          (a, b) =>
            tierRank[a.tier] - tierRank[b.tier] || (listOrder[a.name] ?? 99) - (listOrder[b.name] ?? 99)
        );
        const top = [ranked[1], ranked[0], ranked[2]];
        const shield = mark.id === "physical" ? "is-shield" : "";
        const steps = top
          .map((cls, i) => {
            if (!cls) {
              return `<div class="step ${places[i].key} vacant"><div class="plinth">${places[i].medal}</div></div>`;
            }
            const rarity = data.RARITIES[cls.rarity];
            const tier = data.TIERS.find((t) => t.id === cls.tier);
            return `<div class="step ${places[i].key}" style="--rarity:${rarity?.hex || "#888"}">
              <a class="champ" href="${classHref(cls)}">
                ${icon(cls.archetype)}
                <strong>${cls.name}</strong>
                <em>${tier?.label || cls.tier}</em>
              </a>
              <div class="plinth">${places[i].medal}</div>
            </div>`;
          })
          .join("");

        return `<article class="court">
          <header>
            <img class="${shield}" src="${mark.icon}" alt="">
            <h3>${mark.label}</h3>
          </header>
          <div class="steps">${steps}</div>
        </article>`;
      })
      .join("");
  }

  function render() {
    renderBoard();
    renderPodiums();
  }

  filters.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-rarity]");
    if (!btn) return;
    rarityFilter = btn.dataset.rarity;
    filters.querySelectorAll(".chip").forEach((el) => {
      el.setAttribute("aria-pressed", String(el === btn));
    });
    render();
  });

  search.addEventListener("input", render);
  document.getElementById("source").textContent = data.meta.source;
  document.getElementById("title").textContent = data.meta.title;
  renderLegend();
  renderFilters();
  render();
})();
