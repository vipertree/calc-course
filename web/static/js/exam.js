/* A full-length practice exam, Bluebook style: one part at a time, a countdown per part, a question navigator with
   mark-for-review, and no way back into a finished part. The server owns the clock (course/exams.py): the countdown
   shows the seconds it sent, every answer is saved to it as it is picked, and when time runs out the page asks the
   server for the next state instead of deciding for itself. Once the exam is over the same page is the score report.
   No alert/confirm/prompt anywhere: questions to the student are in-page popups. */
(() => {
  const root = document.getElementById("exam");
  const META = JSON.parse(document.getElementById("exam-meta").textContent);
  let S = JSON.parse(document.getElementById("exam-data").textContent);
  const api = (action) => root.dataset.api.replace(/state\/$/, action + "/");

  // ------------------------------------------------------------ helpers
  const h = (tag, attrs = {}, ...kids) => {
    const el = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "class") el.className = v;
      else if (k === "html") el.innerHTML = v;
      else if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
      else if (v !== false && v != null) el.setAttribute(k, v === true ? "" : v);
    }
    for (const kid of kids.flat()) if (kid != null && kid !== false) el.append(kid.nodeType ? kid : document.createTextNode(kid));
    return el;
  };
  const post = async (action, body = {}) => {
    const r = await fetch(api(action), { method: "POST", credentials: "same-origin",
      headers: { "Content-Type": "application/json", "X-CSRFToken": window.CSRF }, body: JSON.stringify(body) });
    if (r.status >= 500 || r.status === 403 || r.status === 404) throw new Error("server " + r.status);
    return r.json();
  };
  const typeset = (el) => {
    if (!window.renderMathInElement) return;
    window.renderMathInElement(el, { throwOnError: false, delimiters: [
      { left: "$$", right: "$$", display: true }, { left: "\\[", right: "\\]", display: true }, { left: "$", right: "$", display: false }] });
  };
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* storage blocked */ } },
  };
  const figureEl = (f) => {
    if (!f) return null;
    const el = h("figure", {}, h("div", { class: "svg" }), f.caption ? h("figcaption", { html: f.caption }) : null);
    fetch(root.dataset.static + "figures/" + f.src).then((r) => r.text()).then((svg) => { el.firstChild.innerHTML = svg; typeset(el); });
    return el;
  };
  const LETTERS = "ABCD";
  const partRow = (p) => h("div", { class: "exam-part-row" }, h("strong", {}, `(${p.label})`), h("div", { html: p.html }));
  const plural = (n, w) => `${n} ${w}${n === 1 ? "" : "s"}`;
  const partName = (p) => `${p.section}, ${p.name}`;
  const partWhat = (p) => `${p.count} ${p.kind === "mcq" ? "multiple-choice" : "free-response"} question${p.count === 1 ? "" : "s"}, ${p.minutes} minutes, ${p.calc ? "graphing calculator" : "no calculator"}`;

  // an in-page popup in place of confirm(): resolves true for the main button, false for the other or Escape
  function ask(title, body, yes, no = "Keep working") {
    return new Promise((done) => {
      const close = (v) => { back.remove(); document.removeEventListener("keydown", esc); done(v); };
      const esc = (e) => { if (e.key === "Escape") close(false); };
      const yesBtn = h("button", { class: "btn primary", type: "button", onclick: () => close(true) }, yes);
      const back = h("div", { class: "exam-pop-back" }, h("div", { class: "exam-pop card", role: "dialog", "aria-modal": "true", "aria-label": title },
        h("h2", {}, title), ...[].concat(body).map((b) => typeof b === "string" ? h("p", {}, b) : b),
        h("div", { class: "row" }, h("button", { class: "btn", type: "button", onclick: () => close(false) }, no), yesBtn)));
      document.addEventListener("keydown", esc);
      document.body.append(back);
      yesBtn.focus();
    });
  }
  function toast(text) {
    const t = h("div", { class: "exam-toast", role: "status" }, text);
    document.body.append(t);
    setTimeout(() => t.remove(), 6000);
  }

  // ------------------------------------------------------------ dark mode, for the calculator
  const darkQuery = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  const wantsDark = () => { const t = document.documentElement.dataset.theme; return t === "slate" || (t !== "paper" && !!(darkQuery && darkQuery.matches)); };

  // ================================================================ the live exam
  let tick = null, poll = null, deadline = 0, warned = false;

  function live() {
    clearInterval(tick); clearInterval(poll);
    root.replaceChildren();
    document.body.classList.add("in-exam");
    if (S.finished) { location.reload(); return; }
    const part = S.outline[S.part];
    if (!S.running) { intermission(part); return; }
    running(part, S.part);
  }

  function intermission(part) {
    const k = S.part;
    const sectionTwo = k === 2;
    const lead = k === 0
      ? ["Each part has its own clock. It starts when you press Start and keeps running even if you close the page.",
         "When a part's time runs out, or you submit it, you move on and can't go back to it."]
      : sectionTwo
        ? ["Section I is done. Take a break if you need one: the clock for Section II doesn't start until you press Start.",
           "Section II is free response. Write your solutions on paper, with your work shown, as you would in the exam booklet. When the exam is over you score them yourself with the scoring guide."]
        : [`${partName(S.outline[k - 1])} is done.`];
    const rows = S.outline.map((p, i) => h("tr", { class: i < k ? "done" : i === k ? "cur" : "" },
      h("td", {}, partName(p)), h("td", {}, `${p.count} ${p.kind === "mcq" ? "multiple choice" : "free response"}`),
      h("td", {}, `${p.minutes} min`), h("td", {}, p.calc ? "Calculator" : "No calculator"),
      h("td", {}, i < k ? "Done" : i === k ? "Next" : "")));
    const go = h("button", { class: "btn primary", type: "button" }, `Start ${partName(part)}`);
    const msg = h("p", { class: "fb bad", hidden: true });
    go.addEventListener("click", async () => {
      go.disabled = true;
      try { const r = await post("begin"); S = r.state; live(); }
      catch (e) { go.disabled = false; msg.hidden = false; msg.textContent = "That didn't go through. Check your connection and press Start again."; }
    });
    root.append(h("div", { class: "narrow exam-break" },
      h("div", { class: "lesson-head" }, h("span", { class: "chip" }, META.course), h("span", { class: "unit" }, META.title), h("h1", {}, partName(part))),
      h("p", { class: "lede" }, partWhat(part) + "."),
      ...lead.map((t) => h("p", {}, t)),
      part.calc ? h("p", {}, "A graphing calculator opens with the Calculator button at the top of the screen.") : null,
      part.kind === "mcq" ? h("p", {}, "Pick one answer for each question. Answers save as you pick them. There's no penalty for guessing, so answer every question.") : null,
      h("table", { class: "data exam-outline" }, h("tr", {}, ...["Part", "Questions", "Time", "Calculator", ""].map((t) => h("th", {}, t))), ...rows),
      h("div", { class: "row" }, go), msg));
  }

  // ------------------------------------------------------------ a running part
  function running(part, partIndex) {
    const items = S.items;
    const answers = { ...S.answers };
    const flags = new Set(S.flags);
    const posKey = `calc.exam.${S.id}.${part.key}.pos`;
    let pos = Math.min(parseInt(store.get(posKey) || "0", 10) || 0, items.length);   // items.length = the review page
    const pending = {};          // item -> value not yet confirmed by the server
    let saveState = "saved";

    // top bar: part, clock, tools
    const clock = h("span", { class: "exam-clock", "aria-live": "off" });
    const clockBtn = h("button", { class: "linkbtn", type: "button" });
    let clockHidden = store.get("calc.exam.hideclock") === "1";
    const showClock = () => { clock.hidden = clockHidden; clockBtn.textContent = clockHidden ? "Show timer" : "Hide timer"; };
    clockBtn.addEventListener("click", () => { clockHidden = !clockHidden; store.set("calc.exam.hideclock", clockHidden ? "1" : "0"); showClock(); });
    showClock();
    const saved = h("span", { class: "exam-saved muted" });
    const calcBtn = part.calc ? h("button", { class: "btn small", type: "button", onclick: () => calculator() }, "Calculator") : null;
    const bar = h("div", { class: "exam-bar" },
      h("div", { class: "exam-bar-l" }, h("strong", {}, partName(part)), h("span", { class: "muted" }, part.calc ? "Graphing calculator allowed" : "No calculator")),
      h("div", { class: "exam-bar-c" }, clock, clockBtn),
      h("div", { class: "exam-bar-r" }, saved, calcBtn));
    const stage = h("div", { class: "exam-stage" });
    const nav = h("div", { class: "exam-nav" });
    root.append(bar, stage, nav);

    const setSaved = (st) => {
      saveState = st;
      saved.textContent = { saved: "All answers saved", saving: "Saving", retry: "Not saved yet. Retrying" }[st];
      saved.classList.toggle("bad", st === "retry");
    };
    setSaved("saved");
    const pendKey = `calc.exam.${S.id}.pending`;
    const flush = async () => {
      const ids = Object.keys(pending);
      if (!ids.length) { setSaved("saved"); store.set(pendKey, "{}"); return; }
      setSaved("saving");
      for (const id of ids) {
        const v = pending[id];
        try {
          const r = await post("answer", { item: id, value: v });
          if (pending[id] === v) delete pending[id];
          if (!r.ok) {           // the server closed this part: follow it
            S = r.state; toast("This part is over. Your answers up to the end of its time were kept."); live(); return;
          }
        } catch (e) { setSaved("retry"); store.set(pendKey, JSON.stringify(pending)); return; }
      }
      store.set(pendKey, JSON.stringify(pending));
      setSaved(Object.keys(pending).length ? "saving" : "saved");
    };
    // an answer picked just before a reload, which never reached the server: send it now (the server decides if it still counts)
    try { Object.assign(pending, JSON.parse(store.get(pendKey) || "{}")); } catch (e) { /* ignore */ }
    for (const [k, v] of Object.entries(pending)) if (items.some((it) => it.id === k)) answers[k] = v; else delete pending[k];
    flush();
    const retry = setInterval(() => { if (Object.keys(pending).length) flush(); }, 5000);

    const pick = (id, v) => { answers[id] = v; pending[id] = v; store.set(pendKey, JSON.stringify(pending)); flush(); };
    const toggleFlag = (id) => {
      const on = !flags.has(id);
      if (on) flags.add(id); else flags.delete(id);
      post("flag", { item: id, on }).catch(() => {});
      return on;
    };
    const label = (i) => part.kind === "mcq" ? `Question ${items[i].n}` : items[i].title;
    const answered = (it) => part.kind === "mcq" ? !!answers[it.id] : true;

    function show(i) {
      pos = i;
      store.set(posKey, String(i));
      stage.replaceChildren(i >= items.length ? review() : question(items[i]));
      typeset(stage);
      renderNav();
      window.scrollTo({ top: 0 });
    }

    function question(it) {
      const flagBtn = h("button", { class: "exam-flag" + (flags.has(it.id) ? " on" : ""), type: "button", "aria-pressed": flags.has(it.id) ? "true" : "false" },
        h("span", { class: "flag-ico", "aria-hidden": "true" }), "Mark for review");
      flagBtn.addEventListener("click", () => { const on = toggleFlag(it.id); flagBtn.classList.toggle("on", on); flagBtn.setAttribute("aria-pressed", on ? "true" : "false"); renderNav(); });
      const head = h("div", { class: "exam-q-head" }, h("span", { class: "exam-q-n" }, part.kind === "mcq" ? String(it.n) : it.title), flagBtn);
      if (part.kind === "mcq") {
        const ul = h("ul", { class: "choices" });
        it.choices.forEach((c, j) => {
          const L = LETTERS[j];
          const inp = h("input", { type: "radio", name: it.id, value: L });
          if (answers[it.id] === L) inp.checked = true;
          inp.addEventListener("change", () => { pick(it.id, L); renderNav(); });
          ul.append(h("li", {}, h("label", {}, inp, h("span", { class: "L" }, L), h("span", { html: c }))));
        });
        return h("div", { class: "card exam-q" }, head, h("div", { html: it.html }), figureEl(it.figure), ul);
      }
      return h("div", { class: "card exam-q" }, head,
        h("p", { class: "muted small" }, `${it.points} points. Write your solution on paper. Show your work and justify answers where a part asks you to.`),
        h("div", { html: it.html }), figureEl(it.figure),
        ...it.parts.map((p) => h("div", { class: "exam-frq-part" }, partRow(p))));
    }

    function grid(onPick) {
      return h("div", { class: "exam-grid" }, ...items.map((it, i) => h("button", {
        type: "button", class: "exam-cell" + (answered(it) && part.kind === "mcq" ? " answered" : "") + (flags.has(it.id) ? " flagged" : "") + (i === pos ? " cur" : ""),
        "aria-label": `${label(i)}${part.kind === "mcq" ? (answered(it) ? ", answered" : ", unanswered") : ""}${flags.has(it.id) ? ", marked for review" : ""}`,
        onclick: () => onPick(i) }, part.kind === "mcq" ? String(it.n) : String(it.n))));
    }
    const legend = () => h("div", { class: "exam-legend muted" }, part.kind === "mcq" ? h("span", {}, h("i", { class: "exam-cell answered" }), "Answered") : null,
      part.kind === "mcq" ? h("span", {}, h("i", { class: "exam-cell" }), "Unanswered") : null, h("span", {}, h("i", { class: "exam-cell flagged" }), "Marked for review"));

    function review() {
      const blank = items.filter((it) => !answered(it)).length;
      const marked = items.filter((it) => flags.has(it.id)).length;
      const submit = h("button", { class: "btn primary", type: "button", onclick: () => submitPart(false) }, `Submit ${partName(part)}`);
      return h("div", { class: "card exam-review" }, h("h2", {}, "Check your work"),
        h("p", {}, part.kind === "mcq"
          ? `${plural(items.length - blank, "question")} answered${blank ? `, ${blank} unanswered` : ""}${marked ? `, ${marked} marked for review` : ""}. Pick a number to go back to it.`
          : `Make sure your solutions are written down. ${marked ? `${plural(marked, "question")} marked for review. ` : ""}Pick a question to go back to it.`),
        grid(show), legend(),
        h("p", { class: "muted" }, "You can keep working until the time runs out. Once you submit, this part is closed."),
        h("div", { class: "row" }, submit));
    }

    async function submitPart(timeUp) {
      if (!timeUp) {
        const blank = items.filter((it) => !answered(it)).length;
        const ok = await ask(`Submit ${partName(part)}?`, [
          `You won't be able to come back to ${part.kind === "mcq" ? "these questions" : "this part"}.`,
          blank ? `${plural(blank, "question")} still ${blank === 1 ? "has" : "have"} no answer.` : null,
          `There's still time left: ${fmt(Math.max(0, deadline - performance.now()) / 1000)}.`].filter(Boolean), "Submit part");
        if (!ok) return;
      }
      if (timeUp && !stage.classList.contains("time-up")) {      // no more picking while the server closes the part
        stage.classList.add("time-up");
        stage.querySelectorAll("input, button").forEach((el) => { el.disabled = true; });
        nav.querySelectorAll("button").forEach((el) => { el.disabled = true; });
        toast(`Time is up for ${partName(part)}. Saving your answers.`);
      }
      await flush();
      try {
        const r = await post(timeUp ? "state" : "submit", { part: part.key });
        clearInterval(retry);
        S = r.state;
        if (S.finished) { location.reload(); return; }
        if (S.part === partIndex && S.running) {   // the server says time isn't up yet: keep going
          deadline = performance.now() + S.remaining * 1000;
          if (timeUp) setTimeout(() => submitPart(true), 1500);
          return;
        }
        live();
      } catch (e) { setTimeout(() => submitPart(timeUp), 3000); }
    }

    function renderNav() {
      const atReview = pos >= items.length;
      const prev = h("button", { class: "btn", type: "button", disabled: pos === 0, onclick: () => show(pos - 1) }, "Back");
      const next = h("button", { class: "btn primary", type: "button", onclick: () => show(pos + 1), hidden: atReview }, pos === items.length - 1 ? "Review" : "Next");
      const panel = h("div", { class: "exam-nav-panel card", hidden: true }, h("div", { class: "row" }, h("strong", {}, partName(part)),
        h("button", { class: "btn small", type: "button", onclick: () => { panel.hidden = true; } }, "Close")),
        grid((i) => { panel.hidden = true; show(i); }), legend(),
        h("button", { class: "btn small", type: "button", onclick: () => { panel.hidden = true; show(items.length); } }, "Go to the review page"));
      const opener = h("button", { class: "btn exam-nav-open", type: "button", "aria-expanded": "false",
        onclick: () => { panel.hidden = !panel.hidden; opener.setAttribute("aria-expanded", panel.hidden ? "false" : "true"); } },
        atReview ? "Review" : `${label(pos)} of ${items[items.length - 1].n}`);
      nav.replaceChildren(h("div", { class: "exam-nav-in" }, prev, h("div", { class: "exam-nav-mid" }, opener, panel), next));
    }

    // the clock: the server's remaining seconds, counted down on this page's monotonic clock
    deadline = performance.now() + S.remaining * 1000;
    warned = S.remaining <= 300;
    const draw = () => {
      const left = (deadline - performance.now()) / 1000;
      clock.textContent = fmt(Math.max(0, left));
      clock.classList.toggle("low", left <= 300);
      if (!warned && left <= 300) {
        warned = true;
        toast(`5 minutes left in ${partName(part)}.`);
        if (clockHidden) { clockHidden = false; showClock(); }
      }
      if (left <= 0) { clearInterval(tick); clearInterval(poll); submitPart(true); }
    };
    tick = setInterval(draw, 250);
    draw();
    // resync with the server every minute (a laptop that slept has a stale countdown)
    poll = setInterval(async () => {
      try {
        const r = await post("state");
        if (r.state.finished || r.state.part !== S.part || !r.state.running) { clearInterval(tick); clearInterval(poll); clearInterval(retry); S = r.state; if (S.finished) location.reload(); else live(); return; }
        deadline = performance.now() + r.state.remaining * 1000;
      } catch (e) { /* offline: keep counting */ }
    }, 60000);
    show(pos);
  }

  function fmt(sec) {
    sec = Math.ceil(sec);
    const m = Math.floor(sec / 60), s = sec % 60;
    return `${m}:${String(s).padStart(2, "0")}`;
  }

  // the graphing calculator, docked like Bluebook's
  function calculator() {
    let dock = document.querySelector(".desmos-dock");
    if (dock) { const off = dock.classList.toggle("min"); document.body.classList.toggle("has-dock", !off); return; }
    const box = h("div", { class: "desmos-host" });
    const hide = h("button", { class: "btn small", type: "button" }, "Hide");
    dock = h("aside", { class: "desmos-dock", "aria-label": "Graphing calculator" }, h("div", { class: "row" }, h("strong", {}, "Calculator"), hide), box);
    hide.addEventListener("click", () => { dock.classList.add("min"); document.body.classList.remove("has-dock"); });
    dock.querySelector(".row strong").addEventListener("click", () => { if (dock.classList.contains("min")) { dock.classList.remove("min"); document.body.classList.add("has-dock"); } });
    document.body.append(dock);
    document.body.classList.add("has-dock");
    if (window.Desmos) window.Desmos.GraphingCalculator(box, { invertedColors: wantsDark() });
    else box.append(h("p", { class: "muted", style: "padding:12px" }, "The graphing calculator could not load. Use your own graphing calculator for this part."));
  }

  // ================================================================ the score report
  function report() {
    document.body.classList.remove("in-exam");
    const head = h("div", { class: "lesson-head" }, h("span", { class: "chip" }, META.course), h("span", { class: "unit" }, "Score report"), h("h1", {}, META.title));
    const sum = h("div");
    const units = h("div");
    const drawSummary = () => sum.replaceChildren(summaryCard(S.summary));
    const drawUnits = () => units.replaceChildren(unitTable(S.units));
    drawSummary(); drawUnits();
    const jump = h("nav", { class: "exam-jump" }, h("a", { href: "#frq" }, "Score your free response"), h("a", { href: "#mc" }, "Multiple-choice review"), h("a", { href: "#units" }, "By unit"));
    const frq = h("section", { id: "frq" }, h("h2", {}, "Score your free response"),
      h("p", { class: "muted" }, "For each part, compare your written solution with the sample solution, then check each scoring point you earned. "
        + "A point needs what the scoring guide asks for: a setup, a reason, or an answer with units. A matching number alone doesn't earn it. Your scores save as you check them."),
      ...S.frq.map((q) => frqCard(q, () => { drawSummary(); drawUnits(); })));
    const mc = mcReview();
    root.replaceChildren(h("div", { class: "narrow" }, head, sum, jump, frq, mc, h("section", { id: "units" }, h("h2", {}, "By unit"), units),
      h("p", {}, h("a", { class: "btn", href: root.dataset.home }, "Back to the exam page"))));
    typeset(root);
  }

  function summaryCard(s) {
    const left = s.frq_parts - s.frq_parts_scored;
    const cut = s.cutoffs.map(([score, lo], i) => `${score}: ${lo}${i ? ` to ${s.cutoffs[i - 1][1] - 1}` : " and up"}`).concat([`1: below ${s.cutoffs[s.cutoffs.length - 1][1]}`]);
    return h("div", { class: "card exam-summary" },
      h("div", { class: "exam-ap" }, h("span", { class: "exam-ap-n" }, String(s.ap)), h("span", {}, h("strong", {}, "Estimated AP score"),
        h("small", { class: "muted" }, left ? `So far. ${plural(left, "free-response part")} still to score.` : "From all of your scores."))),
      h("dl", { class: "exam-nums" },
        h("dt", {}, "Multiple choice"), h("dd", {}, `${s.mc} / ${s.mc_total}`),
        h("dt", {}, "Free response"), h("dd", {}, `${s.frq} / ${s.frq_total}`),
        h("dt", {}, "Composite"), h("dd", {}, `${fmtNum(s.composite)} / ${s.composite_total}`)),
      h("details", { class: "exam-how" }, h("summary", {}, "How the estimate works"),
        h("p", {}, `The composite counts the two sections equally: multiple-choice points times ${fmtNum(s.composite_total / 2 / s.mc_total)}, plus free-response points. `
          + "The cutoffs below are close to those of past AP Calculus AB exams, but the College Board sets new ones every year, so read the result as a range."),
        h("p", { class: "muted" }, cut.join("; ") + ".")));
  }
  const fmtNum = (v) => (Math.round(v * 10) / 10).toString();

  function frqCard(q, changed) {
    const total = h("strong");
    const upd = () => {
      const got = q.parts.reduce((a, p) => a + (p.marks ? p.rubric.reduce((b, r, k) => b + (p.marks[k] ? r.points : 0), 0) : 0), 0);
      const scored = q.parts.filter((p) => p.marks).length;
      total.textContent = scored ? `${got} / ${q.points}` : `not scored yet / ${q.points}`;
    };
    const card = h("div", { class: "card exam-frq", id: q.id },
      h("div", { class: "tag" }, q.title, h("span", { class: "calc" }, q.calc ? "calculator" : "no calculator"), h("span", { class: "muted", style: "font-weight:400" }, `${q.points} points`)),
      h("div", { html: q.html }), figureEl(q.figure));
    q.parts.forEach((p) => {
      const box = h("div");
      const btn = h("button", { class: "btn small", type: "button" }, "Show the scoring guide");
      const open = () => {
        btn.hidden = true;
        const marks = p.marks ? [...p.marks] : p.rubric.map(() => false);
        const ul = h("ul", { class: "rubric" });
        const status = h("span", { class: "muted small" });
        p.rubric.forEach((line, k) => {
          const cb = h("input", { type: "checkbox", "aria-label": `${line.points} point` });
          cb.checked = !!marks[k];
          cb.addEventListener("change", async () => {
            marks[k] = cb.checked;
            status.textContent = "Saving";
            try {
              const r = await post("frq", { part: p.id, checks: marks });
              if (!r.ok) throw new Error("refused");
              p.marks = [...marks]; S.summary = r.summary; S.units = r.units; upd(); changed(); status.textContent = "Saved";
            } catch (e) { status.textContent = "Not saved. Check your connection and try again."; cb.checked = !cb.checked; marks[k] = cb.checked; }
          });
          ul.append(h("li", {}, h("label", { class: "rubric-line" }, cb, h("span", { class: "pts" }, `${line.points} pt`), h("span", { html: line.html }))));
        });
        box.append(h("div", { class: "solution" }, h("div", { class: "lbl" }, "Sample solution"), h("div", { html: p.solution })),
          h("div", { class: "solution" }, h("div", { class: "lbl" }, "Scoring guide: check each point you earned"), ul, status));
        if (!p.marks) {         // opening the guide counts as scoring: an all-unchecked part is a real 0, saved
          post("frq", { part: p.id, checks: marks }).then((r) => { if (r.ok) { p.marks = [...marks]; S.summary = r.summary; S.units = r.units; upd(); changed(); } }).catch(() => {});
        }
        typeset(box);
      };
      btn.addEventListener("click", open);
      card.append(h("div", { class: "exam-frq-part" }, partRow(p), h("div", { class: "row" }, btn), box));
      if (p.marks) open();
    });
    upd();
    card.append(h("p", { style: "text-align:right" }, "Your score: ", total));
    return card;
  }

  function mcReview() {
    const missed = S.mc.filter((q) => !q.ok).length;
    const only = h("input", { type: "checkbox" });
    const list = h("div", { class: "exam-mc-list" });
    const draw = () => {
      list.replaceChildren(...S.mc.filter((q) => !only.checked || !q.ok).map((q) => {
        const ul = h("ul", { class: "choices" }, ...q.choices.map((c, j) => {
          const L = LETTERS[j];
          return h("li", {}, h("label", { class: (L === q.key ? "right" : L === q.given ? "wrong" : "") },
            h("span", { class: "L" }, L), h("span", { html: c }), L === q.key ? h("span", { class: "tagline" }, "correct answer") : L === q.given ? h("span", { class: "tagline" }, "your answer") : null));
        }));
        return h("details", { class: "card exam-mc" + (q.ok ? "" : " missed") },
          h("summary", {}, h("span", { class: "exam-q-n" }, String(q.n)), h("span", { class: "fb " + (q.ok ? "good" : "bad") }, q.ok ? "Correct" : q.given ? `You chose ${q.given}` : "No answer"),
            h("span", { class: "muted small" }, `Topic ${q.topic}`)),
          h("div", { html: q.html }), figureEl(q.figure), ul,
          h("div", { class: "solution" }, h("div", { class: "lbl" }, "Solution"),
            q.why ? h("p", { html: `<strong>Choice ${q.given} comes from a common slip:</strong> ${q.why}.` }) : null, h("div", { html: q.solution })));
      }));
      typeset(list);
    };
    only.addEventListener("change", draw);
    draw();
    return h("section", { id: "mc" }, h("h2", {}, "Multiple-choice review"),
      h("p", { class: "muted" }, `${S.summary.mc} of ${S.summary.mc_total} right. Open a question to see the solution.`),
      missed ? h("label", { class: "exam-only" }, only, ` Only the ${plural(missed, "question")} I missed`) : null, list);
  }

  function unitTable(us) {
    return h("div", { class: "table-wrap" }, h("table", { class: "data exam-units" },
      h("tr", {}, h("th", {}, "Unit"), h("th", {}, "Multiple choice"), h("th", {}, "Free response"), h("th", {}, "Lessons to review")),
      ...us.map((u) => h("tr", {}, h("td", {}, `${u.n}. ${u.title}`), h("td", {}, `${u.mc} / ${u.mc_total}`),
        h("td", {}, u.frq_total ? `${u.frq} / ${u.frq_total}` : h("span", { class: "muted" }, "not scored yet")),
        h("td", {}, u.review.length ? h("ul", { class: "exam-review-list" }, ...u.review.map((r) => h("li", {},
          h("span", { class: "chip-sm" }, r.n), " ", r.ready ? h("a", { href: root.dataset.topic.replace("0.0", r.n) }, r.title) : h("span", {}, r.title))))
          : h("span", { class: "muted" }, "Nothing missed"))))));
  }

  // ------------------------------------------------------------ start (KaTeX loads with defer)
  const start = () => (S.finished ? report() : live());
  if (window.renderMathInElement) start();
  else {
    const t0 = Date.now();
    const t = setInterval(() => { if (window.renderMathInElement || Date.now() - t0 > 5000) { clearInterval(t); start(); } }, 30);
  }
})();
