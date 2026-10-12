// Every page: typeset inline $...$ math in .mathy elements once KaTeX's auto-render has loaded.
// (Was an onload= attribute; the Content-Security-Policy allows no inline handlers.)
(function () {
  if (!window.renderMathInElement) return;
  document.querySelectorAll(".mathy").forEach((e) => window.renderMathInElement(e, {
    throwOnError: false, delimiters: [{ left: "$", right: "$", display: false }] }));
})();

// main navigation: open on wide screens, a Menu button on narrow ones; one dropdown open at a time
(function () {
  const fold = document.querySelector(".nav-fold");
  const mq = window.matchMedia("(max-width: 1180px)");
  const top = document.querySelector(".top");
  const bar = top && top.querySelector(".in");
  // wider than 1180px the bar can still overflow (links style, a signed-in name, a wide design font): measure it
  // with the links laid out in a row and fold into the Menu button when they don't fit (.nav-tight, app.css)
  const measure = () => {
    if (!bar || mq.matches) { if (top) top.classList.remove("nav-tight"); return; }
    top.classList.remove("nav-tight");
    if (fold) fold.open = true;
    top.classList.toggle("nav-tight", bar.scrollWidth > bar.clientWidth + 1);
  };
  const narrow = { get matches() { return mq.matches || !!(top && top.classList.contains("nav-tight")); } };
  const groups = [...document.querySelectorAll(".nav-group")];
  // inside the narrow Menu every group stays open as a labelled list; on wide screens they are dropdowns
  const sync = () => { measure(); if (fold) fold.open = !narrow.matches; groups.forEach((g) => { g.open = narrow.matches; }); };
  sync();
  mq.addEventListener ? mq.addEventListener("change", sync) : mq.addListener(sync);
  let t = 0, lastW = window.innerWidth;
  // width changes only: a phone's address bar resizes the height while scrolling, and that must not shut the Menu
  window.addEventListener("resize", () => { if (window.innerWidth === lastW) return; lastW = window.innerWidth;
    clearTimeout(t); t = setTimeout(sync, 120); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(sync);
  groups.forEach((g) => g.addEventListener("toggle", () => {
    if (g.open && !narrow.matches) groups.forEach((o) => { if (o !== g) o.open = false; });
  }));
  document.addEventListener("click", (e) => {
    if (!narrow.matches) groups.forEach((g) => { if (g.open && !g.contains(e.target)) g.open = false; });
    if (fold && narrow.matches && fold.open && !fold.contains(e.target)) fold.open = false;
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !narrow.matches) groups.forEach((g) => { g.open = false; }); });
})();
