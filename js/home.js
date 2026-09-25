(function () {
  const site = window.SITE;
  if (!site) return;

  const stage = document.getElementById("rotator");
  if (stage) {
    const slides = [1, 2, 3, 4].map(
      (n) => `assets/img/home/MainPhoto${n}.webp?v=15`
    );
    stage.innerHTML = slides
      .map(
        (src, i) =>
          `<img src="${src}" alt="Dungeon LootR" ${i === 0 ? "class=\"is-on\"" : ""}>`
      )
      .join("") + `<div class="rotator-dots" id="rotator-dots"></div>`;

    const imgs = [...stage.querySelectorAll("img")];
    const dots = document.getElementById("rotator-dots");
    dots.innerHTML = slides
      .map((_, i) => `<button type="button" aria-label="Slide ${i + 1}" ${i === 0 ? "class=\"is-on\"" : ""}></button>`)
      .join("");
    const buttons = [...dots.querySelectorAll("button")];
    let i = 0;
    const show = (next) => {
      imgs[i].classList.remove("is-on");
      buttons[i].classList.remove("is-on");
      i = (next + imgs.length) % imgs.length;
      imgs[i].classList.add("is-on");
      buttons[i].classList.add("is-on");
    };
    buttons.forEach((btn, idx) => btn.addEventListener("click", () => show(idx)));
    setInterval(() => show(i + 1), 5200);
  }
})();
