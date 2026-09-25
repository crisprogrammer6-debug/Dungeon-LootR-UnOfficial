(function () {
  const site = window.SITE;
  const key = document.body.dataset.placeholder;
  if (!site || !key) return;
  const copy = site.placeholders[key];
  if (!copy) return;
  const title = document.getElementById("title");
  const kicker = document.getElementById("kicker");
  const body = document.getElementById("lead");
  if (title) title.textContent = copy.title;
  if (kicker) kicker.textContent = copy.kicker;
  if (body) body.textContent = copy.body || "";
})();
