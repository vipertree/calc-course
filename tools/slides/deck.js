// Teacher slide deck: keyboard and clicker navigation, fullscreen, light/dark looks, silent clips.
// Clickers send PageDown/PageUp (or the arrow keys), and some send "b" or "." to black the screen.
(function () {
  const stage = document.querySelector(".stage");
  const slides = [...document.querySelectorAll(".slide")];
  const chrome = document.querySelector(".chrome");
  const count = document.querySelector(".chrome .count");
  const keys = document.querySelector(".keys");
  const black = document.querySelector(".blackout");
  const params = new URLSearchParams(location.search);
  const shot = params.has("shot");
  let cur = -1;

  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private window: the choice just isn't kept */ } },
  };

  // ---------------------------------------------------------------- looks
  // The page opens in the site's look (the server writes data-theme from the site's cookie), else the device's.
  const root = document.documentElement;
  if (params.get("theme")) root.dataset.theme = params.get("theme");
  else if (!root.dataset.theme && store.get("deck-theme")) root.dataset.theme = store.get("deck-theme");
  const look = () => (getComputedStyle(root).colorScheme.includes("dark") ? "dark" : "light");
  function toggleTheme() {
    root.dataset.theme = look() === "dark" ? "paper" : "slate";
    store.set("deck-theme", root.dataset.theme);
    loadClips(slides[cur]);
  }

  // ---------------------------------------------------------------- scaling
  function scaleStage() {
    const s = Math.min(innerWidth / 1920, innerHeight / 1080);
    stage.style.transform = `translate(${-960 * s}px, ${-540 * s}px) scale(${s})`;
  }
  // a slide's main column shrinks its content to fit, never grows it
  function fit(slide) {
    slide.querySelectorAll(".main").forEach((main) => {
      const box = main.querySelector(".fit");
      if (!box) return;
      box.style.transform = "";
      box.style.width = "100%";
      const h = box.scrollHeight, w = box.scrollWidth, H = main.clientHeight, W = main.clientWidth;
      const s = Math.min(1, H / h, W / w);
      if (s < 1) {
        box.style.width = `${100 / s}%`;            // re-flow at the smaller size so lines use the full width
        const s2 = Math.min(1, H / box.scrollHeight, W / box.scrollWidth);
        box.style.transform = `scale(${s2})`;
      }
    });
  }

  // ---------------------------------------------------------------- clips
  function loadClips(slide) {
    if (!slide) return;
    slide.querySelectorAll("video[data-light]").forEach((v) => {
      const want = (look() === "dark" && v.dataset.dark) ? v.dataset.dark : v.dataset.light;
      const poster = (look() === "dark" && v.dataset.posterDark) ? v.dataset.posterDark : v.dataset.posterLight;
      if (v.getAttribute("src") !== want) {
        const t = v.currentTime || 0;
        v.setAttribute("src", want);
        if (poster) v.setAttribute("poster", poster);
        if (t) v.addEventListener("loadedmetadata", () => { v.currentTime = t; }, { once: true });
      }
    });
  }
  function stopClips(slide) {
    if (slide) slide.querySelectorAll("video").forEach((v) => v.pause());
  }

  // ---------------------------------------------------------------- navigation
  function go(n) {
    n = Math.max(0, Math.min(slides.length - 1, n));
    if (n === cur) return;
    if (cur >= 0) { slides[cur].classList.remove("on"); stopClips(slides[cur]); }
    cur = n;
    const s = slides[cur];
    s.classList.add("on");
    fit(s);
    if (!shot) loadClips(s);
    count.textContent = `${cur + 1} / ${slides.length}`;
    if (!shot) history.replaceState(null, "", "#" + (cur + 1));
  }
  const next = () => go(cur + 1), prev = () => go(cur - 1);

  function fullscreen() {
    if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen().catch(() => {});
  }
  function playPause() {
    const v = slides[cur].querySelector("video");
    if (v) (v.paused ? v.play() : v.pause());
  }

  document.addEventListener("keydown", (e) => {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    const inVideo = e.target instanceof HTMLVideoElement;
    if (!keys.hidden && e.key !== "?") { keys.hidden = true; e.preventDefault(); return; }
    switch (e.key) {
      case "ArrowRight": case "ArrowDown": case "PageDown": case "Enter": case "n": case "N":
        if (inVideo && (e.key === "ArrowRight" || e.key === "ArrowLeft")) return;   // seeking inside a clip
        next(); break;
      case " ":
        if (inVideo) return;
        e.shiftKey ? prev() : next(); break;
      case "ArrowLeft": case "ArrowUp": case "PageUp": case "Backspace": case "p": case "P":
        if (inVideo && e.key === "ArrowLeft") return;
        prev(); break;
      case "Home": go(0); break;
      case "End": go(slides.length - 1); break;
      case "f": case "F": fullscreen(); break;
      case "t": case "T": toggleTheme(); break;
      case "k": case "K": playPause(); break;
      case "b": case "B": case ".": black.hidden = !black.hidden; break;
      case "?": keys.hidden = !keys.hidden; break;
      default: return;
    }
    e.preventDefault();
  });
  keys.addEventListener("click", () => { keys.hidden = true; });
  black.addEventListener("click", () => { black.hidden = true; });
  chrome.addEventListener("click", (e) => {
    const b = e.target.closest("[data-act]");
    if (!b) return;
    ({ prev, next, full: fullscreen, theme: toggleTheme, keys: () => { keys.hidden = false; } })[b.dataset.act]();
    b.blur();
  });

  // controls show while the mouse moves and fade after a moment of stillness
  let idle;
  const wake = () => {
    chrome.classList.remove("idle");
    clearTimeout(idle);
    idle = setTimeout(() => chrome.classList.add("idle"), 2500);
  };
  document.addEventListener("mousemove", wake);
  wake();

  addEventListener("resize", () => { scaleStage(); if (cur >= 0) fit(slides[cur]); });
  addEventListener("hashchange", () => go(parseInt(location.hash.slice(1), 10) - 1 || 0));

  // ---------------------------------------------------------------- start (after the math is typeset)
  if (shot) document.body.classList.add("shot");
  window.deckTypeset = function () {
    if (window.renderMathInElement) {
      window.renderMathInElement(stage, { throwOnError: false, delimiters: [
        { left: "$$", right: "$$", display: true }, { left: "\\[", right: "\\]", display: true },
        { left: "$", right: "$", display: false }] });
    }
    const start = () => {
      scaleStage();
      const n = cur < 0 ? (parseInt(location.hash.slice(1), 10) - 1 || 0) : cur;
      slides.forEach((s) => s.classList.remove("on"));
      cur = -1;
      go(n);                  // re-fit now that the math has its real size
      document.body.dataset.ready = "1";
    };
    (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(start);
  };
  scaleStage();
  go(parseInt(location.hash.slice(1), 10) - 1 || 0);

  // for the PowerPoint export (tools/slides/shoot.py): show slide n, and where its title and clip sit
  window.deckGo = (n) => { go(n); return slides.length; };
  window.deckInfo = () => {
    const s = slides[cur];
    const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect(); return { x: b.left, y: b.top, w: b.width, h: b.height }; };
    const title = s.querySelector(".title.plain");
    return { title: r(title), titleText: title ? title.textContent.trim() : "", video: r(s.querySelector(".clip video")),
             errors: s.querySelectorAll(".katex-error").length, scale: (s.querySelector(".fit") || {}).style?.transform || "" };
  };
})();
