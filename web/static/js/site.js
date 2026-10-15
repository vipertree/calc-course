// Every page: typeset inline $...$ math in .mathy elements once KaTeX's auto-render has loaded.
// (Was an onload= attribute; the Content-Security-Policy allows no inline handlers.)
(function () {
  if (!window.renderMathInElement) return;
  document.querySelectorAll(".mathy").forEach((e) => window.renderMathInElement(e, {
    throwOnError: false, delimiters: [{ left: "$", right: "$", display: false }] }));
})();

// main navigation: three dropdowns in a row; when they don't fit (a phone, a signed-in name, a narrow window) they
// fold behind the hamburger button. Measured, not a fixed breakpoint (Adder 2026-10-15: fold only once text is cut off).
(function () {
  const fold = document.querySelector(".nav-fold");
  const top = document.querySelector(".top");
  const bar = top && top.querySelector(".in");
  const measure = () => {
    if (!bar) return;
    top.classList.remove("nav-tight");
    if (fold) fold.open = true;
    top.classList.toggle("nav-tight", bar.scrollWidth > bar.clientWidth + 1);
  };
  const narrow = { get matches() { return !!(top && top.classList.contains("nav-tight")); } };
  const groups = [...document.querySelectorAll(".nav-group")];
  // inside the narrow Menu every group stays open as a labelled list; on wide screens they are dropdowns
  const sync = () => { measure(); if (fold) fold.open = !narrow.matches; groups.forEach((g) => { g.open = narrow.matches; }); };
  sync();
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

  // course flyouts (Adder 2026-10-15): AP Calc Course > units > lessons. Mouse: open on hover, but switching to a
  // neighbouring unit waits a moment so a diagonal move toward the lessons panel doesn't flip it. Keyboard: arrow
  // right/down opens and steps in, up/down move, left or Escape steps back out. Off on phones and in the folded Menu.
  const subs = [...document.querySelectorAll(".site-nav .has-sub")];
  if (!subs.length) return;
  const owner = (el) => el.parentElement.closest(".has-sub");       // the item whose panel this one sits in
  const peers = (it) => subs.filter((o) => o !== it && owner(o) === owner(it));
  const isOpen = (it) => it.classList.contains("open");
  const linkOf = (it) => it.querySelector(":scope > a");
  const panelLinks = (panel) => [...panel.querySelectorAll(":scope > a, :scope > .nav-item > a")];
  const place = (it) => {      // keep an opened panel on screen: shift a top panel left, flip a nested one
    const panel = it.querySelector(":scope > .nav-sub");
    panel.classList.remove("flip"); panel.style.left = "";
    const r = panel.getBoundingClientRect(), room = document.documentElement.clientWidth - 8;
    if (r.right <= room) return;
    if (owner(it) || it.closest(".nav-drop")) panel.classList.add("flip");
    else panel.style.left = `${Math.max(-r.left + 8, room - r.right)}px`;
  };
  const setOpen = (it, on) => {
    it.classList.toggle("open", on);
    if (on) place(it);
    linkOf(it).setAttribute("aria-expanded", on ? "true" : "false");
    if (!on) it.querySelectorAll(".has-sub.open").forEach((c) => setOpen(c, false));
  };
  const openOnly = (it) => { peers(it).forEach((o) => { if (isOpen(o)) setOpen(o, false); }); setOpen(it, true); };
  const closeAll = () => subs.forEach((it) => { if (isOpen(it)) setOpen(it, false); });
  let pending = 0;
  subs.forEach((it) => {
    it.addEventListener("pointerenter", (e) => {
      if (e.pointerType !== "mouse" || narrow.matches) return;
      clearTimeout(it.closing); clearTimeout(pending);
      if (isOpen(it)) return;
      pending = setTimeout(() => openOnly(it), peers(it).some(isOpen) ? 220 : 60);
    });
    it.addEventListener("pointerleave", (e) => {
      if (e.pointerType !== "mouse") return;
      clearTimeout(pending);
      it.closing = setTimeout(() => setOpen(it, false), 400);
    });
    it.addEventListener("focusout", (e) => { if (!it.contains(e.relatedTarget)) setOpen(it, false); });
  });
  const nav = document.querySelector(".site-nav");
  nav.addEventListener("keydown", (e) => {
    if (narrow.matches) return;
    const a = e.target.closest("a");
    if (!a) return;
    const item = a.parentElement.classList.contains("has-sub") && linkOf(a.parentElement) === a ? a.parentElement : null;
    const panel = a.parentElement.closest(".nav-sub");
    const inPanel = panel && (a.parentElement === panel || a.parentElement.parentElement === panel);
    const go = (el) => { if (el) { e.preventDefault(); e.stopPropagation(); el.focus(); } };
    const stepIn = item && (e.key === "ArrowRight" || (e.key === "ArrowDown" && !inPanel));
    if (stepIn) { openOnly(item); return go(panelLinks(item.querySelector(":scope > .nav-sub"))[0]); }
    if (!inPanel) return;
    const list = panelLinks(panel), i = list.indexOf(a);
    if (e.key === "ArrowDown") return go(list[(i + 1) % list.length]);
    if (e.key === "ArrowUp") return go(list[(i - 1 + list.length) % list.length]);
    if (e.key === "ArrowLeft" || e.key === "Escape") {
      const up = panel.parentElement; setOpen(up, false); return go(linkOf(up));
    }
  });
  document.addEventListener("click", (e) => { if (!nav.contains(e.target)) closeAll(); });
  groups.forEach((g) => g.addEventListener("toggle", () => { if (!g.open) g.querySelectorAll(".has-sub.open").forEach((it) => setOpen(it, false)); }));
  window.addEventListener("resize", closeAll);
})();

// light/dark switch: flips the page in place and stores the choice through the same /theme/ link it falls back to
(function () {
  const sw = document.querySelector(".theme-switch");
  if (!sw) return;
  const root = document.documentElement;
  const isDark = () => root.dataset.theme ? root.dataset.theme === "slate"
    : window.matchMedia("(prefers-color-scheme: dark)").matches;
  const show = () => {
    const dark = isDark();
    sw.setAttribute("aria-checked", dark ? "true" : "false");
    sw.href = `${dark ? sw.dataset.light : sw.dataset.dark}?next=${encodeURIComponent(location.pathname + location.search)}`;
  };
  show();
  sw.addEventListener("click", (e) => {
    e.preventDefault();
    const next = isDark() ? "paper" : "slate";
    fetch(next === "slate" ? sw.dataset.dark : sw.dataset.light, { credentials: "same-origin", redirect: "manual" }).catch(() => {});
    root.dataset.theme = next;
    show();
  });
  sw.addEventListener("keydown", (e) => { if (e.key === " ") { e.preventDefault(); sw.click(); } });
})();
