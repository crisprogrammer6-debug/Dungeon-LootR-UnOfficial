(function () {
  const form = document.getElementById("suggest-form");
  const status = document.getElementById("suggest-status");
  const count = document.getElementById("suggest-count");
  const bodyEl = document.getElementById("suggest-body");
  const cfg = window.SUGGESTIONS || {};
  if (!form || !status) return;

  function setStatus(text, kind) {
    status.textContent = text;
    status.dataset.kind = kind || "";
  }

  function tickCount() {
    if (!count || !bodyEl) return;
    count.textContent = `${bodyEl.value.length} / 1000`;
  }

  if (bodyEl) bodyEl.addEventListener("input", tickCount);
  tickCount();

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const body = String(form.body.value || "").trim();
    const discord = String(form.discord.value || "").trim();
    if (body.length < 4) {
      setStatus("Write a bit more before sending.", "err");
      return;
    }
    if (!cfg.endpoint) {
      setStatus("Could not send right now.", "err");
      return;
    }

    const payload = {
      type: "suggestion",
      body: body.slice(0, 1000),
      discord: discord.slice(0, 80),
      sentAt: new Date().toISOString(),
    };

    const btn = form.querySelector("button[type='submit']");
    if (btn) btn.disabled = true;
    setStatus("Sending…", "");

    try {
      const res = await fetch(cfg.endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        setStatus("Could not send right now.", "err");
        return;
      }
      form.reset();
      tickCount();
      setStatus("Sent. Thank you.", "ok");
    } catch (err) {
      setStatus("Could not send right now. Try again later.", "err");
    } finally {
      if (btn) btn.disabled = false;
    }
  });
})();
