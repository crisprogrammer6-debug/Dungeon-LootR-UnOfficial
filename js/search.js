(function () {
  const index = window.SEARCH_INDEX;
  const host = document.getElementById("site-search");
  if (!index || !host) return;

  const input = host.querySelector("input");
  const list = host.querySelector(".site-search-results");
  if (!input || !list) return;

  function norm(s) {
    return String(s || "")
      .toLowerCase()
      .replace(/['’]/g, "")
      .replace(/[^a-z0-9]+/g, " ")
      .trim();
  }

  const groups = (index.synonymGroups || []).map((g) => g.map(norm).filter(Boolean));

  function expand(q) {
    const tokens = norm(q).split(/\s+/).filter(Boolean);
    const out = new Set(tokens);
    for (const token of tokens) {
      if (token.length < 2) continue;
      for (const group of groups) {
        const hit = group.some((term) => term === token || term.split(" ").includes(token) || (token.length >= 3 && term.includes(token)));
        if (hit) group.forEach((t) => out.add(t));
      }
    }
    return [...out];
  }

  function score(rec, raw, terms) {
    const title = norm(rec.title);
    const hay = norm(rec.keys || rec.title);
    const q = norm(raw);
    if (!q) return 0;
    let n = 0;
    if (title === q) n += 120;
    else if (title.startsWith(q)) n += 90;
    else if (title.includes(q)) n += 70;
    if (hay.includes(q)) n += 25;
    let hits = 0;
    for (const t of terms) {
      if (t.length < 2) continue;
      if (title.includes(t) || hay.includes(t)) hits += 1;
    }
    if (hits) n += hits * 12;
    return n;
  }

  function render(items) {
    if (!items.length) {
      list.hidden = false;
      list.innerHTML = `<p class="site-search-empty">No matches.</p>`;
      return;
    }
    list.hidden = false;
    list.innerHTML = items
      .map(
        (r) =>
          `<a href="${r.href}"><span class="site-search-kind">${r.kind}</span><span class="site-search-title">${r.title}</span></a>`
      )
      .join("");
  }

  function run() {
    const raw = input.value.trim();
    if (raw.length < 2) {
      list.hidden = true;
      list.innerHTML = "";
      return;
    }
    const terms = expand(raw);
    const ranked = index.records
      .map((r) => ({ r, n: score(r, raw, terms) }))
      .filter((x) => x.n > 0)
      .sort((a, b) => b.n - a.n || a.r.title.localeCompare(b.r.title))
      .slice(0, 12)
      .map((x) => x.r);
    render(ranked);
  }

  input.addEventListener("input", run);
  input.addEventListener("focus", run);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      list.hidden = true;
      input.blur();
    }
    if (e.key === "Enter") {
      const first = list.querySelector("a");
      if (first && !list.hidden) {
        e.preventDefault();
        location.href = first.getAttribute("href");
      }
    }
  });
  document.addEventListener("click", (e) => {
    if (!host.contains(e.target)) list.hidden = true;
  });
})();
