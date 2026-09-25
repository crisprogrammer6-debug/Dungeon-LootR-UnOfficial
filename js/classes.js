(function () {
  const catalog = window.CLASS_CATALOG;
  const root = document.getElementById("class-root");
  if (!catalog || !root) return;

  const params = new URLSearchParams(location.search);
  const id = params.get("id");
  const cls = catalog.classes.find((c) => c.id === id);

  const rarityHex = (r) => catalog.rarities[r]?.hex || "#d4b15a";
  const rarityLabel = (r) => catalog.rarities[r]?.label || r;

  function panelsFor(entry) {
    const list = [
      { id: "class-info", label: "Class info" },
      { id: "skill-info", label: "Skill info" },
      { id: "mastery-info", label: "Mastery info" },
    ];
    if (entry.hasPassive) list.push({ id: "mastery-passive", label: "Mastery passive" });
    if (entry.hasEvolve) list.push({ id: "evolve", label: "Evolve" });
    return list;
  }

  function title(entry) {
    return `<h2 class="gc-title" style="color:${rarityHex(entry.rarity)};text-shadow:0 0 18px ${rarityHex(entry.rarity)}66">${entry.name}</h2>`;
  }

  function chevron(dir) {
    const d =
      dir === "left"
        ? "M20 5 L8 14 L20 23 M34 5 L22 14 L34 23"
        : "M6 5 L18 14 L6 23 M20 5 L32 14 L20 23";
    return `<svg class="gc-chev" viewBox="0 0 40 28" aria-hidden="true"><path d="${d}" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/></svg>`;
  }

  function footer(entry, current, left, right) {
    return `<nav class="gc-foot">
      <button type="button" class="gc-side" data-go="${left?.id || ""}" ${left ? "" : "disabled"} aria-label="${left ? left.label : ""}">
        ${chevron("left")}
      </button>
      <div class="gc-now">${current.label}</div>
      <button type="button" class="gc-side gc-next" data-go="${right?.id || ""}" ${right ? "" : "disabled"} aria-label="${right ? right.label : ""}">
        ${chevron("right")}
      </button>
    </nav>`;
  }

  function card(inner, extra) {
    return `<article class="game-card${extra ? ` ${extra}` : ""}">
      <span class="gc-frame" aria-hidden="true"></span>
      <span class="gc-c tl"></span><span class="gc-c tr"></span>
      <span class="gc-c bl"></span><span class="gc-c br"></span>
      <span class="gc-jewel top"></span><span class="gc-jewel bot"></span>
      <span class="gc-jewel left"></span><span class="gc-jewel right"></span>
      ${inner}<div class="gc-mark" aria-hidden="true"></div>
    </article>`;
  }

  function evolve(entry, nav) {
    const paths = entry.evolve || [];
    const body = paths.length
      ? `<div class="gc-skills">${paths
          .map((ev) => {
            const name = ev.href
              ? `<a class="obtain-hi" href="${ev.href}">${ev.name}</a>`
              : ev.name;
            const npc = ev.npcHref
              ? `<a class="obtain-hi" href="${ev.npcHref}">${ev.npc}</a>`
              : ev.npc;
            const awards = ev.awards
              ? ev.awardsHref
                ? `<a class="obtain-hi" href="${ev.awardsHref}">${ev.awards}</a>`
                : ev.awards
              : "";
            return `<div class="gc-skill">
              <div>
                <strong>${name}</strong>
                <p>Via ${npc}. ${ev.req}${awards ? ` Awards: ${awards}.` : ""}</p>
              </div>
            </div>`;
          })
          .join("")}</div>`
      : `<p class="gc-empty"> </p>`;
    return card(`${title(entry)}
      <p class="gc-kicker">Evolve</p>
      ${body}
      ${footer(entry, nav.current, nav.left, nav.right)}`);
  }

  function weapons(entry) {
    const files = entry.weapons || [];
    if (!files.length) return "";
    const srcs = files.map((file) =>
      file.includes("/") ? file : `assets/img/weapons/${file}`
    );
    const cls = srcs.length > 1 ? "gc-weapons is-pair" : "gc-weapons";
    return `<div class="${cls}">${srcs
      .map((s, i) => `<img class="${i === 1 ? "is-spear" : ""}" src="${s}" alt="">`)
      .join("")}</div>`;
  }

  function classInfo(entry, nav) {
    const s = entry.stats;
    return card(`${title(entry)}
      <div class="gc-info-split">
        <div class="gc-info-left">
          <p class="gc-label">Rarity:</p>
          <p class="gc-rarity" style="color:${rarityHex(entry.rarity)}">${rarityLabel(entry.rarity)}</p>
          <p class="gc-label gc-obtain-k">How to obtain:</p>
          <p class="gc-obtain">${entry.obtain}</p>
          <p class="gc-stats-k">STATS:</p>
          <div class="gc-vitals">
            <span>
              <svg class="gc-ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="#e8e8ee" d="M12 21s-6.6-4.35-9.2-8.1C.7 9.9 2.1 6 5.6 6c2 0 3.2 1.1 3.9 2.2C10.3 7.1 11.5 6 13.5 6c3.5 0 4.9 3.9 2.8 6.9C18.6 16.65 12 21 12 21z"/></svg>
              ${s.hp}<small>Health</small>
            </span>
            <span>
              <svg class="gc-ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="#cfd3dc" d="M20.7 3.3l-5.2 1.2-8.6 8.6 3.3 3.3 8.6-8.6 1.2-5.2-3.3.7zm-11 13.1L6.4 13.1 3 16.5 2 22l5.5-1 3.2-3.6z"/></svg>
              ${s.atk}<small>Attack</small>
            </span>
          </div>
          <div class="gc-stats">
            <span class="is-str">+${s.str} STR</span>
            <span>+${s.dex} DEX</span>
            <span>+${s.vit} VIT</span>
            <span>+${s.int} INT</span>
            <span>+${s.lck} LCK</span>
          </div>
        </div>
        <div class="gc-info-right">
          <p class="gc-label">Archetype:</p>
          <p class="gc-arch">${entry.archetype}</p>
          ${weapons(entry)}
        </div>
      </div>
      ${footer(entry, nav.current, nav.left, nav.right)}`, "is-info");
  }

  function skillInfo(entry, nav) {
    return card(`${title(entry)}
      <p class="gc-kicker">SKILLS INFO:</p>
      <div class="gc-skills">
        ${entry.skills
          .map(
            (sk) => `<div class="gc-skill">
              <div>
                <strong>${sk.name}</strong>
                <p>${sk.text}</p>
              </div>
              <div class="gc-mult">
                ${sk.tag ? `<em>${sk.tag}</em>` : ""}
                <span>${sk.mult}</span>
              </div>
            </div>`
          )
          .join("")}
      </div>
      ${footer(entry, nav.current, nav.left, nav.right)}`);
  }

  function masteryInfo(entry, nav) {
    return card(`${title(entry)}
      <p class="gc-kicker">MASTERY UNLOCKS:</p>
      <div class="gc-masteries">
        ${entry.masteries
          .map(
            (m) => `<div class="gc-mastery">
              <div class="gc-ml">
                <span>LEVEL ${m.level}</span>
                <b>LOCKED</b>
              </div>
              <p>${m.text}</p>
            </div>`
          )
          .join("")}
      </div>
      ${footer(entry, nav.current, nav.left, nav.right)}`);
  }

  function masteryPassive(entry, nav) {
    const p = entry.passive;
    return card(`${title(entry)}
      <div class="gc-pass-top">
        <div>
          <p class="gc-label">Rarity:</p>
          <p class="gc-rarity" style="color:${rarityHex(entry.rarity)}">${rarityLabel(entry.rarity)}</p>
        </div>
        <div class="gc-crest"></div>
        <div class="gc-meta-right">
          <p class="gc-label">Archetype:</p>
          <p>${entry.archetype}</p>
        </div>
      </div>
      <h3 class="gc-pass-name">${p.name}</h3>
      <p class="gc-pass-text">${p.text}</p>
      <p class="gc-locked">LOCKED - Reach Level: ${p.unlockLevel}</p>
      ${footer(entry, nav.current, nav.left, nav.right)}`);
  }

  function navBundle(entry, panelId) {
    const list = panelsFor(entry);
    const i = Math.max(0, list.findIndex((p) => p.id === panelId));
    return { list, current: list[i], left: list[i - 1], right: list[i + 1], i };
  }

  function renderDetail(entry, panelId) {
    const nav = navBundle(entry, panelId);
    const tabs = nav.list
      .map(
        (p) =>
          `<button class="chip" data-panel="${p.id}" aria-pressed="${p.id === nav.current.id}">${p.label}</button>`
      )
      .join("");

    let body = "";
    if (nav.current.id === "class-info") body = classInfo(entry, nav);
    else if (nav.current.id === "skill-info") body = skillInfo(entry, nav);
    else if (nav.current.id === "mastery-info") body = masteryInfo(entry, nav);
    else if (nav.current.id === "mastery-passive") body = masteryPassive(entry, nav);
    else body = evolve(entry, nav);

    root.innerHTML = `
      <p class="back-row"><a href="classes.html">← All classes</a></p>
      <div class="filters class-panels">${tabs}</div>
      ${body}`;
  }

  function renderList(filter) {
    const order = catalog.rarityOrder;
    const chips = [{ id: "all", label: "All" }, ...order.map((id) => ({ id, label: rarityLabel(id) }))]
      .map(
        (t) =>
          `<button class="chip" data-rarity="${t.id}" aria-pressed="${t.id === filter}">${t.label}</button>`
      )
      .join("");

    const list = catalog.classes
      .slice()
      .sort((a, b) => order.indexOf(a.rarity) - order.indexOf(b.rarity))
      .filter((c) => filter === "all" || c.rarity === filter);

    const tile = (c) =>
      `<a class="class-tile" href="classes.html?id=${c.id}" style="--rarity:${rarityHex(c.rarity)}">
        <strong>${c.name}</strong>
        <span>${rarityLabel(c.rarity)} · ${c.archetype}</span>
      </a>`;

    let body = "";
    if (filter === "all") {
      body = order
        .map((rid) => {
          const group = list.filter((c) => c.rarity === rid);
          if (!group.length) return "";
          return `<section class="rarity-block">
            <div class="rarity-rule"><i></i><span>${rarityLabel(rid)}</span><i></i></div>
            <div class="class-grid">${group.map(tile).join("")}</div>
          </section>`;
        })
        .join("");
    } else {
      body = `<div class="class-grid">${list.map(tile).join("")}</div>`;
    }

    root.innerHTML = `<div class="filters" id="class-filters">${chips}</div>${body}`;
  }

  function currentFilter() {
    return params.get("rarity") || "all";
  }

  function currentPanel() {
    const p = params.get("panel");
    if (!p || p === "obtainment") return "class-info";
    return p;
  }

  root.addEventListener("click", (e) => {
    const rarity = e.target.closest("[data-rarity]");
    if (rarity) {
      history.replaceState(null, "", `classes.html?rarity=${rarity.dataset.rarity}`);
      params.set("rarity", rarity.dataset.rarity);
      renderList(rarity.dataset.rarity);
      return;
    }
    const panel = e.target.closest("[data-panel], [data-go]");
    if (panel && cls) {
      const next = panel.dataset.panel || panel.dataset.go;
      if (!next) return;
      history.replaceState(null, "", `classes.html?id=${cls.id}&panel=${next}`);
      renderDetail(cls, next);
    }
  });

  if (cls) renderDetail(cls, currentPanel());
  else renderList(currentFilter());
})();
