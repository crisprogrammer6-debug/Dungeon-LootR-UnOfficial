(function () {
  const topics = window.TOPICS;
  const root = document.getElementById("topic-root");
  const key = document.body.dataset.topics;
  if (!topics || !root || !key) return;
  const list = topics[key] || [];

  function shotLabel(src, index) {
    const file = String(src).split("/").pop().split("?")[0].toLowerCase();
    if (file.includes("shop")) return "Shop";
    if (file.includes("ui")) return "Interface";
    return index === 0 ? "Event" : "Extra";
  }

  function shotsFor(item) {
    return [item.image].concat(item.extra || []);
  }

  function renderEvents(items) {
    if (!items.length) return;
    let active = 0;
    let shot = 0;

    function applyHash() {
      const hash = (location.hash || "").replace(/^#/, "");
      if (!hash) return;
      const shop = hash.endsWith("-shop");
      const id = shop ? hash.slice(0, -5) : hash;
      const idx = items.findIndex((ev) => ev.id === id);
      if (idx >= 0) {
        active = idx;
        shot = shop && (items[idx].extra || []).length ? 1 : 0;
      }
    }

    applyHash();

    root.innerHTML = `<div class="event-board">
      <div class="event-switch" role="tablist" aria-label="Events"></div>
      <article class="event-stage">
        <div class="event-hero">
          <div class="event-frame" aria-hidden="true"></div>
          <img alt="">
        </div>
        <aside class="event-side">
          <h2></h2>
          <div class="event-thumbs"></div>
        </aside>
        <div class="topic-info event-dossier">
          <p class="topic-info-label">Info</p>
          <div class="topic-info-body"></div>
        </div>
      </article>
    </div>`;

    const switcher = root.querySelector(".event-switch");
    const hero = root.querySelector(".event-hero img");
    const title = root.querySelector(".event-side h2");
    const thumbs = root.querySelector(".event-thumbs");
    const info = root.querySelector(".event-dossier .topic-info-body");

    switcher.innerHTML = items
      .map(
        (ev, i) =>
          `<button type="button" role="tab" aria-selected="false" data-event="${i}">${ev.title}</button>`
      )
      .join("");

    function paint() {
      const item = items[active];
      const gallery = shotsFor(item);
      if (shot >= gallery.length) shot = 0;
      const src = gallery[shot];

      switcher.querySelectorAll("[data-event]").forEach((btn, i) => {
        const on = i === active;
        btn.classList.toggle("is-on", on);
        btn.setAttribute("aria-selected", on ? "true" : "false");
      });

      if (hero.getAttribute("src") !== src) hero.src = src;
      hero.alt = `${item.title} — ${shotLabel(src, shot)}`;
      title.textContent = item.title;
      info.innerHTML = item.info || `<p class="event-empty">Details coming soon.</p>`;

      if (thumbs.dataset.for !== item.id) {
        thumbs.dataset.for = item.id;
        thumbs.innerHTML = gallery
          .map(
            (img, i) => `<button type="button" class="event-thumb" data-shot="${i}">
            <img src="${img}" alt="">
            <span>${shotLabel(img, i)}</span>
          </button>`
          )
          .join("");
      }

      thumbs.querySelectorAll(".event-thumb").forEach((btn, i) => {
        const on = i === shot;
        btn.classList.toggle("is-on", on);
        btn.setAttribute("aria-pressed", on ? "true" : "false");
      });
    }

    root.addEventListener("click", (event) => {
      const tab = event.target.closest("[data-event]");
      if (tab) {
        active = Number(tab.dataset.event);
        shot = 0;
        paint();
        return;
      }
      const thumb = event.target.closest("[data-shot]");
      if (thumb) {
        shot = Number(thumb.dataset.shot);
        paint();
      }
    });

    paint();
    window.addEventListener("hashchange", () => {
      applyHash();
      paint();
    });
  }

  if (key === "events") {
    renderEvents(list);
    return;
  }

  root.innerHTML = list
    .map(
      (item) => `<article class="topic-card${item.wide ? " is-wide" : ""}" id="${item.id}">
        <h2>${item.title}</h2>
        <div class="topic-shot">
          <img src="${item.image}" alt="${item.title}">
        </div>
        ${(item.extra || [])
          .map(
            (src) => `<div class="topic-shot is-extra"><img src="${src}" alt=""></div>`
          )
          .join("")}
        <div class="topic-info">
          <p class="topic-info-label">Info</p>
          <div class="topic-info-body">${item.info ? (String(item.info).trim().startsWith("<") ? item.info : `<p>${item.info}</p>`) : ""}</div>
        </div>
      </article>`
    )
    .join("");

  const hash = (location.hash || "").replace(/^#/, "");
  if (hash) {
    const target = document.getElementById(hash);
    if (target) {
      target.classList.add("is-target");
      requestAnimationFrame(() => target.scrollIntoView({ behavior: "smooth", block: "center" }));
    }
  }
})();
