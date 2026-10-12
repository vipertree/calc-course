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
  const narrow = window.matchMedia("(max-width: 1180px)");
  const groups = [...document.querySelectorAll(".nav-group")];
  // inside the narrow Menu every group stays open as a labelled list; on wide screens they are dropdowns
  const sync = () => { if (fold) fold.open = !narrow.matches; groups.forEach((g) => { g.open = narrow.matches; }); };
  sync();
  narrow.addEventListener ? narrow.addEventListener("change", sync) : narrow.addListener(sync);
  groups.forEach((g) => g.addEventListener("toggle", () => {
    if (g.open && !narrow.matches) groups.forEach((o) => { if (o !== g) o.open = false; });
  }));
  document.addEventListener("click", (e) => {
    if (!narrow.matches) groups.forEach((g) => { if (g.open && !g.contains(e.target)) g.open = false; });
    if (fold && narrow.matches && fold.open && !fold.contains(e.target)) fold.open = false;
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !narrow.matches) groups.forEach((g) => { g.open = false; }); });
})();
