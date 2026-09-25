(function () {
  const extras = window.EXTRAS;
  const site = window.SITE;
  const panel = document.getElementById("extras-panel");
  if (!extras || !site || !panel) return;

  panel.innerHTML = (site.extrasTabs || [])
    .map((tab) => {
      const copy = extras[tab.id] || { title: tab.label, html: "" };
      return `<article class="topic-info extras-card">
        <p class="topic-info-label">${copy.title}</p>
        <div class="topic-info-body">${copy.html}</div>
      </article>`;
    })
    .join("");
})();
