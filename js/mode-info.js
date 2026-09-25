(function () {
  document.querySelectorAll("[data-rotator]").forEach((stage) => {
    const imgs = [...stage.querySelectorAll("img")];
    if (imgs.length < 2) return;

    let dots = stage.querySelector(".rotator-dots");
    if (!dots) {
      dots = document.createElement("div");
      dots.className = "rotator-dots";
      stage.appendChild(dots);
    }

    dots.innerHTML = imgs
      .map(
        (_, idx) =>
          `<button type="button" aria-label="Slide ${idx + 1}"${idx === 0 ? ' class="is-on"' : ""}></button>`
      )
      .join("");
    const buttons = [...dots.querySelectorAll("button")];
    let i = 0;

    const show = (next) => {
      imgs[i].classList.remove("is-on");
      buttons[i].classList.remove("is-on");
      i = ((next % imgs.length) + imgs.length) % imgs.length;
      imgs[i].classList.add("is-on");
      buttons[i].classList.add("is-on");
    };

    buttons.forEach((btn, idx) => btn.addEventListener("click", () => show(idx)));
    setInterval(() => show(i + 1), 3200);
    imgs[0].classList.add("is-on");
  });
})();
