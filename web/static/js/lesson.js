/* Renders one lesson area from the JSON Django embeds. Answers never ship to the page:
   every check is a POST to /api/<topic>/check/, which returns correctness and, once a
   student has tried, the worked solution. No alert/confirm/prompt anywhere. */
(() => {
  const app = document.getElementById("app");
  const L = JSON.parse(document.getElementById("lesson").textContent);
  const S = JSON.parse(document.getElementById("state").textContent);
  const area = app.dataset.area;
  const correctSet = new Set(S.correct);

  const lockedCard = (what) => h("div", { class: "card locked-card" },
    h("div", { class: "tag" }, "Members only"),
    h("p", {}, `${what} come with a membership. Videos and the first few practice problems are free for everyone.`),
    h("p", {}, h("a", { class: "btn primary", href: "/join/" }, "Join with a class code"), " ",
      h("a", { class: "btn", href: "/login/?next=" + encodeURIComponent(location.pathname) }, "Sign in")));

  // ------------------------------------------------------------ helpers
  const h = (tag, attrs = {}, ...kids) => {
    const el = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "class") el.className = v;
      else if (k === "html") el.innerHTML = v;
      else if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
      else if (v !== false && v != null) el.setAttribute(k, v === true ? "" : v);
    }
    for (const kid of kids.flat()) if (kid != null) el.append(kid.nodeType ? kid : document.createTextNode(kid));
    return el;
  };
  const post = async (url, body) => {
    const r = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json", "X-CSRFToken": window.CSRF },
      body: JSON.stringify(body), credentials: "same-origin" });
    if (!r.ok) throw new Error("server " + r.status);
    return r.json();
  };
  const typeset = (el) => {
    if (!window.renderMathInElement) return;
    window.renderMathInElement(el, { throwOnError: false, delimiters: [
      { left: "$$", right: "$$", display: true }, { left: "\\[", right: "\\]", display: true },
      { left: "$", right: "$", display: false }] });
  };
  const fb = (el, ok, text) => { el.className = "fb " + (ok === true ? "good" : ok === false ? "bad" : "info"); el.textContent = text; el.hidden = false; };
  const mathField = (placeholder = "") => {
    if (!window.customElements.get("math-field")) return h("input", { type: "text", placeholder, "aria-label": "Your answer" });
    const mf = h("math-field", { "math-virtual-keyboard-policy": "auto", "aria-label": "Your answer" });
    mf.addEventListener("focusin", () => { lastMath = mf; kbdButton().hidden = false; });
    mf.setAttribute("placeholder", placeholder);
    mf.smartFence = true;
    return mf;
  };
  let lastMath = null, kbd = null;
  function kbdButton() {
    if (kbd) return kbd;
    kbd = h("button", { class: "kbd-btn", type: "button", hidden: true, "aria-label": "Show or hide the math keyboard" }, "Math keyboard");
    kbd.addEventListener("mousedown", (e) => e.preventDefault());   // keep focus in the field
    kbd.addEventListener("click", () => {
      const vk = window.mathVirtualKeyboard;
      if (!vk) return;
      if (vk.visible) vk.hide(); else { lastMath && lastMath.focus(); vk.show(); }
    });
    document.body.append(kbd);
    return kbd;
  }
  // units live beside the box, so students type only the number
  const unitTag = (u) => u ? h("span", { class: "units", html: "$" + u + "$" }) : null;
  const valueOf = (field) => field.tagName === "MATH-FIELD" ? field.getValue("ascii-math") : field.value;
  const solutionBox = (html, label = "Solution") => { const d = h("div", { class: "solution" }, h("div", { class: "lbl" }, label), h("div", { html })); typeset(d); return d; };

  const ICONS = {
    da: '<svg viewBox="0 0 42 30"><path d="M3 26 Q 20 24 38 6" fill="none" stroke="var(--func)" stroke-width="2.5"/><text x="7" y="13" font-size="11" fill="var(--tangent)" font-style="italic">d/dt</text></svg>',
    dg: '<svg viewBox="0 0 42 30"><path d="M3 26 Q 20 24 38 6" fill="none" stroke="var(--func)" stroke-width="2.5"/><path d="M8 29 L 38 13" stroke="var(--tangent)" stroke-width="2.5"/><circle cx="24" cy="20.6" r="2.4" fill="currentColor"/></svg>',
    ia: '<svg viewBox="0 0 42 30"><path d="M3 26 Q 20 24 38 6" fill="none" stroke="var(--func)" stroke-width="2.5"/><text x="6" y="16" font-size="15" fill="var(--area)">∫</text></svg>',
    ig: '<svg viewBox="0 0 42 30"><path d="M8 27 L8 24.6 Q 20 23 32 13 L32 27 Z" fill="var(--area)" opacity=".75"/><path d="M3 26 Q 20 24 38 6" fill="none" stroke="var(--func)" stroke-width="2.5"/></svg>',
  };
  const MEAN = { da: ["Instantaneous rate of change", "How fast is it changing right now?"],
    dg: ["Slope of the tangent line", "How steep is the graph at a point?"],
    ia: ["Accumulation", "How much has built up?"], ig: ["Area under the curve", "What region does it fill?"] };

  function meanings(b) {
    const on = new Set(b.keys);
    const cell = (k) => h("div", { class: "c" + (on.has(k) ? " on" : ""), html: ICONS[k] + `<span><b>${MEAN[k][0]}</b><small>${MEAN[k][1]}</small></span>` });
    const grid = h("div", { class: "meanings" },
      h("span", { class: "blankh" }), h("span", { class: "h" }, "Analytically"), h("span", { class: "h" }, "Graphically"),
      h("span", { class: "r", style: "color:var(--deriv)" }, "Derivative"), cell("da"), cell("dg"),
      // no integral row until the course gets there (Unit 6)
      ...(["ia", "ig", "inv"].some((k) => on.has(k))
        ? [h("span", { class: "r", style: "color:var(--area)" }, "Integral"), cell("ia"), cell("ig")] : []));
    return h("div", { class: "block" }, grid, b.caption ? h("div", { class: "meanings-cap", html: b.caption }) : null);
  }

  // ------------------------------------------------------------ blanks
  function wireBlanks(root) {
    root.querySelectorAll(".blank[data-blank]").forEach((span) => {
      const id = span.dataset.blank;
      const input = span.dataset.kind === "math" ? mathField() : h("input", { type: "text", autocomplete: "off", "aria-label": "Fill in the blank" });
      span.append(input);
      let tries = 0;
      const reveal = h("button", { class: "reveal", type: "button", hidden: true }, "show");
      span.append(reveal);
      const done = (answerTex) => {
        span.classList.remove("bad"); span.classList.add("good");
        if (answerTex && !valueOf(input)) { const s = h("span", { class: "shown", html: answerTex }); typeset(s); input.replaceWith(s); }
        reveal.hidden = true;
      };
      if (correctSet.has(id)) { span.classList.add("good"); }
      const submit = async () => {
        const given = valueOf(input).trim();
        if (!given) return;
        const r = await post(app.dataset.check, { item: id, given, area: "notes" });
        if (r.correct) done();
        else { tries += 1; span.classList.add("bad"); if (tries >= 1) reveal.hidden = false; }
      };
      input.addEventListener("change", submit);
      // turn green as soon as the typed answer is right; wrong answers are only flagged on Enter or leaving the field
      let timer = null;
      input.addEventListener("input", () => {
        clearTimeout(timer);
        if (span.classList.contains("good")) return;
        timer = setTimeout(async () => {
          const given = valueOf(input).trim();
          if (!given) return;
          const r = await post(app.dataset.check, { item: id, given, area: "notes", live: true });
          if (r.correct && valueOf(input).trim() === given) done();
        }, 700);
      });
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); submit(); } });
      reveal.addEventListener("click", async () => {
        const r = await post(app.dataset.check, { item: id, given: "", reveal: true, area: "notes" });
        if (input.tagName === "INPUT") input.value = ""; else input.setValue("");
        done(r.answer);
      });
    });
  }

  // ------------------------------------------------------------ gradable card (check, practice, FRQ part)
  function answerCard(item, { area: ar, cls = "card q", tagText, extra } = {}) {
    const card = h("div", { class: cls, id: item.id });
    const tag = h("div", { class: "tag" }, tagText || "", item.calc ? h("span", { class: "calc" }, "calculator") : null);
    card.append(tag, h("div", { html: item.html }));
    if (item.figure) card.append(figureEl(item.figure));
    const out = h("div");
    const status = h("span", { class: "fb", hidden: true });
    const row = h("div", { class: "row" });
    let shown = false;
    const showSolution = (r) => {
      if (shown) return; shown = true;
      out.append(solutionBox(r.solution + (r.display ? `<div class="muted" style="margin-top:6px">Answer: $${r.display}$</div>` : "")));
      typeset(out);
    };
    if (item.answer_kind === "self") {
      const btn = h("button", { class: "btn", type: "button", onclick: async () => {
        btn.disabled = true; showSolution(await post(app.dataset.check, { item: item.id, given: "", reveal: true, area: ar }));
      } }, "Show solution");
      row.append(btn, h("span", { class: "muted" }, "Work it out first, then compare."));
    } else {
      const mf = mathField();
      const check = h("button", { class: "btn primary", type: "button" }, "Check");
      const give = h("button", { class: "btn", type: "button", hidden: true }, "Show solution");
      let tries = 0;
      const go = async () => {
        const given = valueOf(mf).trim();
        if (!given) { fb(status, null, "Type an answer first."); return; }
        const r = await post(app.dataset.check, { item: item.id, given, area: ar });
        tries += 1;
        if (r.saved) { fb(status, null, "Answer saved. Your teacher will release results."); return; }
        if (r.correct) { fb(status, true, "Correct"); showSolution(r); }
        else { fb(status, false, tries === 1 ? "Not quite. Try again." : "Still not it."); give.hidden = false; }
      };
      check.addEventListener("click", go);
      mf.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); go(); } });
      give.addEventListener("click", async () => showSolution(await post(app.dataset.check, { item: item.id, given: "", reveal: true, area: ar })));
      row.append(...[mf, unitTag(item.units), check, give, status].filter(Boolean));
      if (correctSet.has(item.id)) fb(status, true, "Done before");
    }
    if (item.calc) row.append(desmosButton(card));
    card.append(row, out);
    if (extra) card.append(extra);
    typeset(card);
    return card;
  }

  function desmosButton(card) {
    let box = null;
    return h("button", { class: "btn small", type: "button", onclick: () => {
      if (box) { box.hidden = !box.hidden; return; }
      box = h("div", { class: "desmos-box" });
      card.append(box);
      if (window.Desmos) window.Desmos.GraphingCalculator(box, { invertedColors: document.documentElement.dataset.theme === "slate" });
      else box.append(h("p", { class: "muted", style: "padding:12px" }, "The graphing calculator could not load."));
    } }, "Calculator");
  }

  function figureEl(f) {
    if (!f) return null;
    const el = h("figure", {}, h("div", { class: "svg" }), f.caption ? h("figcaption", { html: f.caption }) : null);
    fetch(app.dataset.static + "figures/" + f.src).then((r) => r.text()).then((svg) => { el.firstChild.innerHTML = svg; });
    return el;
  }

  // ------------------------------------------------------------ video helpers
  // videos come through the Range-capable /video/ view so the scrubber can seek
  const videoUrl = (src) => app.dataset.video ? app.dataset.video.replace(/X$/, src.replace(/^video\//, "")) : app.dataset.static + src;
  // playback speed is the viewer's choice and carries over from video to video
  function rememberSpeed(v) {
    let saved = null;
    try { saved = parseFloat(localStorage.getItem("calc.videoRate")); } catch (e) { /* storage blocked */ }
    const apply = () => { if (saved > 0) { v.defaultPlaybackRate = saved; v.playbackRate = saved; } };
    apply();
    v.addEventListener("loadedmetadata", apply);
    v.addEventListener("ratechange", () => {
      saved = v.playbackRate;
      try { localStorage.setItem("calc.videoRate", String(v.playbackRate)); } catch (e) { /* storage blocked */ }
    });
  }

  // ------------------------------------------------------------ notes blocks
  function block(b) {
    switch (b.type) {
      case "text": return h("div", { class: "block", html: b.html });
      case "formula": return h("div", { class: "block formula" }, h("span", { class: "tag", html: b.title }), h("div", { html: b.html }));
      case "definition": return h("div", { class: "block definition" }, h("div", { class: "tag", html: b.title }), h("div", { html: b.html }));
      case "bigidea": return h("div", { class: "block bigidea", html: b.html });
      case "meanings": return meanings(b);
      case "figure": { const f = figureEl(b); f.classList.add("block"); return f; }
      case "figrow": return h("div", { class: "block figrow" }, ...b.figures.map(figureEl));
      case "table": return h("div", { class: "block table-wrap", html: b.html });
      case "video": {
        const v = h("video", { controls: true, preload: "metadata", playsinline: true, src: videoUrl(b.src) });
        v.append(h("track", { kind: "captions", srclang: "en", label: "English", src: videoUrl(b.captions), default: true }));
        const box = h("div", { class: "video" }, v);
        v.addEventListener("error", () => box.append(h("div", { class: "missing" }, "This video hasn't been published yet.")));
        rememberSpeed(v);
        return h("div", { class: "block" }, box);
      }
      case "desmos": {
        const box = h("div", { class: "desmos-box" });
        const card = h("div", { class: "block card" }, h("div", { class: "tag", html: "Explore · " + b.title }), h("div", { html: b.html }), box);
        requestAnimationFrame(() => {
          if (!window.Desmos) { box.append(h("p", { class: "muted", style: "padding:12px" }, "Interactive graph unavailable.")); return; }
          const calc = window.Desmos.GraphingCalculator(box, { expressionsCollapsed: false, settingsMenu: false, zoomButtons: true,
            keypad: false, invertedColors: document.documentElement.dataset.theme === "slate" });
          b.expressions.forEach((e) => calc.setExpression(e));
          calc.setMathBounds(b.bounds);
        });
        return card;
      }
      case "example": {
        const out = h("div");
        const btn = h("button", { class: "btn", type: "button", onclick: async () => {
          btn.disabled = true;
          const r = await post(app.dataset.check, { item: b.id, given: "", reveal: true, area: "notes" });
          out.append(solutionBox(r.solution)); btn.hidden = true;
        } }, "Show the solution");
        return h("div", { class: "block card" }, h("div", { class: "tag", html: `Example ${b.n} · ${b.title}` }), h("div", { html: b.html }),
          h("p", { class: "muted", style: "margin:6px 0" }, "Try it yourself first, then compare."), btn, out);
      }
      case "check": return answerCard(b, { area: "notes", cls: "block card check", tagText: "Check your understanding" });
    }
    return h("div", {}, "unknown block " + b.type);
  }

  // ------------------------------------------------------------ areas
  function notes() {
    const videos = L.steps.flatMap((st) => st.blocks.filter((b) => b.type === "video"));
    const side = h("aside", { class: "side" });
    const videoBox = h("div", { class: "side-video" }, ...videos.map(block));
    const hideBtn = h("button", { class: "btn small side-toggle", type: "button" }, "Hide video");
    hideBtn.addEventListener("click", () => { const off = videoBox.hidden = !videoBox.hidden; hideBtn.textContent = off ? "Show video" : "Hide video"; });
    side.append(videoBox, hideBtn);
    if (L.preview) {
      side.classList.add("preview");
      app.append(h("div", { class: "lesson-grid" },
        h("div", {}, h("div", { class: "goals", html: "<strong>Goal.</strong> " + L.goals }),
          lockedCard("The guided notes for this lesson"),
          h("p", {}, h("a", { class: "btn", href: location.pathname + "practice/" }, "Try the free practice problems"))), side));
      typeset(app);
      return;
    }
    // the whole lesson is on the page: no gating. Progress saves when the end of a section scrolls into view.
    const done = new Set(S.steps_done);
    const rail = h("ol");
    const bar = h("i");
    const main = h("div");
    const steps = L.steps.map((st, i) => {
      const sec = h("section", { class: "step", id: "step-" + i },
        h("h2", {}, h("span", { class: "n" }, String(i + 1)), h("span", { html: st.title })),
        ...st.blocks.filter((b) => b.type !== "video").map(block));
      const end = h("div", { class: "step-end", "data-i": String(i) });
      sec.append(end);
      return sec;
    });
    L.steps.forEach((st, i) => rail.append(h("li", { html: st.title, onclick: () => steps[i].scrollIntoView({ behavior: "smooth" }) })));
    const refresh = (cur) => {
      [...rail.children].forEach((li, i) => { li.classList.toggle("done", done.has(i)); li.classList.toggle("cur", i === cur); });
      bar.style.width = (100 * done.size / L.steps.length) + "%";
    };
    const markDone = (i) => {
      if (done.has(i)) return;
      done.add(i); refresh(current);
      post(app.dataset.step, { step: i }).catch(() => {});
    };
    let current = 0;
    if ("IntersectionObserver" in window) {
      const ends = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) markDone(+e.target.dataset.i); }));
      steps.forEach((sec) => ends.observe(sec.querySelector(".step-end")));
      const heads = new IntersectionObserver((es) => es.forEach((e) => {
        if (e.isIntersecting) { current = steps.indexOf(e.target); refresh(current); }
      }), { rootMargin: "0px 0px -60% 0px" });
      steps.forEach((sec) => heads.observe(sec));
    }
    side.append(h("div", { class: "rail" }, rail, h("div", { class: "bar" }, bar), h("div", { class: "muted", style: "font-size:.8rem" }, "Progress saves as you read.")));
    main.append(h("div", { class: "goals", html: "<strong>Goal.</strong> " + L.goals }), ...steps,
      h("div", { class: "step-foot" }, h("a", { class: "btn primary", href: location.pathname + "practice/" }, "On to practice")));
    app.append(h("div", { class: "lesson-grid" }, main, side));
    typeset(main); typeset(rail); wireBlanks(main); refresh(0);
  }

  function practice() {
    const list = h("div", { class: "items narrow" }, h("p", { class: "muted" },
      "Enter your final answer and press Check. Give exact answers unless a problem says to round. "
      + "Type math the way you'd write it: 3x^2, sqrt(x), pi, and / for fractions."));
    L.practice.forEach((it) => list.append(answerCard(it, { area: "practice" }), h("div", { style: "height:14px" })));
    if (L.preview) list.append(lockedCard("The rest of the practice set, the notes, AP test prep and quizzes"));
    app.append(list);
  }

  function quiz(opts = {}) {
    const wrap = h("div", { class: "narrow" });
    if (L.preview) { app.append(h("div", { class: "narrow" }, lockedCard("Quizzes"))); return; }
    const fields = {};
    const cards = L.quiz.map((it) => {
      const card = h("div", { class: "card q", id: it.id }, h("div", { class: "tag" }, it.calc ? h("span", { class: "calc" }, "calculator") : null), h("div", { html: it.html }), figureEl(it.figure));
      if (it.type === "mcq") {
        const ul = h("ul", { class: "choices" });
        it.choices.forEach((c, j) => { const L_ = "ABCD"[j];
          ul.append(h("li", {}, h("label", {}, h("input", { type: "radio", name: it.id, value: L_ }), h("span", { class: "L" }, L_), h("span", { html: c })))); });
        card.append(ul);
        fields[it.id] = () => (card.querySelector("input:checked") || {}).value || "";
      } else {
        const mf = mathField(); card.append(h("div", { class: "row" }, ...[mf, unitTag(it.units)].filter(Boolean)));
        fields[it.id] = () => valueOf(mf);
      }
      card.append(h("div", { class: "result" }));
      typeset(card);
      return card;
    });
    const status = h("div");
    const A = S.assess || { mode: "individual" };
    const what = opts.what || "quiz";
    const showResults = (r, again) => {
      wrap.querySelectorAll(".test-part[hidden]").forEach((s) => { s.hidden = false; });
      wrap.querySelectorAll(".part-gate").forEach((g) => g.remove());
      status.replaceChildren(h("div", { class: "card" }, h("div", { class: "score" }, `${r.score} / ${r.total}`),
        h("p", { class: "muted" }, r.score === r.total ? "Every question right." : (again ? "Review the solutions below, then try again." : "Review the solutions below.")),
        again ? h("button", { class: "btn", type: "button", onclick: () => location.reload() }, "Take it again") : null));
      cards.forEach((card) => {
        const d = r.detail[card.id]; const res = card.querySelector(".result");
        if (!d) return;
        const it = L.quiz.find((q) => q.id === card.id);
        if (it.type === "mcq") card.querySelectorAll("label").forEach((lb) => {
          const inp = lb.querySelector("input");
          if (inp.value === d.given) { lb.classList.add(d.correct ? "right" : "wrong"); inp.checked = true; }
          inp.disabled = true;
        });
        else { const mf = card.querySelector("math-field, input"); if (mf) { if (mf.tagName === "MATH-FIELD") mf.setValue(d.given || ""); else mf.value = d.given || ""; mf.readOnly = true; mf.setAttribute("read-only", ""); } }
        res.replaceChildren(h("p", {}, h("span", { class: "fb " + (d.correct ? "good" : "bad") }, d.correct ? "Correct" : "Incorrect")),
          solutionBox(d.solution + (d.display ? `<div class="muted" style="margin-top:6px">Answer: $${d.display}$</div>` : "")));
      });
    };
    const waiting = () => h("div", { class: "card" }, h("h2", { style: "margin-top:0" }, "Submitted"),
      h("p", {}, `Your ${what} is handed in. Your teacher will release your score and the solutions after everyone has taken it.`));
    if (A.mode === "class" && A.submitted && !A.released) {
      wrap.append(waiting()); app.append(wrap); return;
    }
    const submit = h("button", { class: "btn primary", type: "button" }, `Submit ${what}`);
    submit.addEventListener("click", async () => {
      const answers = Object.fromEntries(Object.entries(fields).map(([k, f]) => [k, f()]));
      const blank = Object.values(answers).filter((v) => !v).length;
      if (blank && !submit.dataset.sure) { submit.dataset.sure = "1"; status.replaceChildren(h("p", { class: "fb bad" }, `${blank} question${blank > 1 ? "s are" : " is"} blank. Press Submit again to hand it in anyway.`)); return; }
      submit.disabled = true;
      let r;
      try { r = await post(app.dataset.quiz, { answers }); }
      catch (e) { submit.disabled = false; status.replaceChildren(h("p", { class: "fb bad" }, "That didn't go through. Check your connection and press Submit again.")); return; }
      if (r.submitted && !r.released) { wrap.replaceChildren(waiting()); wrap.scrollIntoView({ behavior: "smooth" }); return; }
      showResults(r, A.mode !== "class");
      status.scrollIntoView({ behavior: "smooth" });
    });
    const prev = S.quiz.length ? h("p", { class: "muted" }, "Earlier attempts: " + S.quiz.map((a) => `${a.score}/${a.total}`).join(", ")) : null;
    const intro = (opts.intro || "No calculator unless a question says so.") + (A.mode === "class"
      ? ` Everyone in ${A.class_name || "your class"} takes the same ${what}${A.form ? ` (form ${A.form})` : ""}. You can submit once, and your teacher releases the results.`
      : ` You see every answer after you submit, and each attempt draws new versions of the questions.`);
    const released = A.mode === "class" && A.released && A.result;
    const head = h("p", { class: "muted" }, released ? `Results released by your teacher${A.form ? ` (form ${A.form})` : ""}.` : intro);
    if (opts.split) {
      // unit tests: Part 1 (no calculator) must be finished before Part 2 (calculator) opens
      const sec = (part) => h("div", { class: "items" }, ...cards.filter((c, i) => L.quiz[i].part === part).flatMap((c) => [c, h("div", { style: "height:14px" })]));
      const p1 = h("section", { class: "test-part" }, h("h2", {}, "Part 1: no calculator"), sec("A"));
      const p2 = h("section", { class: "test-part" }, h("h2", {}, "Part 2: calculator allowed"), sec("B"));
      const go = h("button", { class: "btn primary", type: "button" }, "Finish Part 1 and start Part 2");
      const gate = h("div", { class: "card part-gate" },
        h("p", { style: "margin-top:0" }, "When you start Part 2, your Part 1 answers are locked in and the calculator opens. You can't go back."),
        h("div", { class: "row" }, go));
      const openPart2 = () => {
        p1.querySelectorAll("input, math-field, textarea, button").forEach((el) => {
          el.disabled = true; if (el.tagName === "MATH-FIELD") el.setAttribute("read-only", "");
        });
        p1.classList.add("locked");
        gate.remove(); p2.hidden = false; calculatorDock(); p2.scrollIntoView({ behavior: "smooth" });
      };
      go.addEventListener("click", openPart2);
      const showAll = released || A.mode !== "class";
      p2.hidden = true;
      p2.append(released ? null : h("div", { class: "row" }, submit), status);
      wrap.append(head, ...(prev ? [prev] : []), p1, gate, p2);
      app.append(wrap);
      opts.split({ p1, p2, gate, unlock: () => { gate.remove(); p2.hidden = false; }, showAll });
      if (released) { gate.remove(); p2.hidden = false; }
    } else {
      const withHeads = cards.flatMap((c, i) => {
        const q = L.quiz[i], prevQ = L.quiz[i - 1];
        const head = q.part && (!prevQ || prevQ.part !== q.part)
          ? h("h2", {}, q.part === "A" ? "Part A: no calculator" : "Part B: calculator allowed") : null;
        return [head, c, h("div", { style: "height:14px" })];
      });
      wrap.append(head, ...(prev ? [prev] : []), h("div", { class: "items" }, ...withHeads.filter(Boolean)),
        released ? null : h("div", { class: "row" }, submit), status);
      app.append(wrap);
    }
    if (released) showResults(A.result, false);
  }

  function testprep() {
    const wrap = h("div", { class: "narrow" });
    if (L.preview) { app.append(h("div", { class: "narrow" }, lockedCard("AP test prep questions"))); return; }
    wrap.append(h("h2", {}, "Multiple choice"), h("p", { class: "muted" }, "AP-style questions. Pick an answer and check it; wrong answers explain the mistake behind them."));
    const mcqs = h("div", { class: "items" });
    L.mcq.forEach((it) => {
      const card = h("div", { class: "card q", id: it.id }, h("div", { class: "tag" }, it.calc ? h("span", { class: "calc" }, "calculator") : null), h("div", { html: it.html }), figureEl(it.figure));
      const ul = h("ul", { class: "choices" });
      it.choices.forEach((c, j) => { const L_ = "ABCD"[j];
        ul.append(h("li", {}, h("label", {}, h("input", { type: "radio", name: it.id, value: L_ }), h("span", { class: "L" }, L_), h("span", { html: c })))); });
      const out = h("div"); const status = h("span", { class: "fb", hidden: true });
      const btn = h("button", { class: "btn primary", type: "button" }, "Check");
      btn.addEventListener("click", async () => {
        const sel = card.querySelector("input:checked");
        if (!sel) { fb(status, null, "Pick an answer first."); return; }
        const r = await post(app.dataset.check, { item: it.id, given: sel.value, area: "testprep" });
        card.querySelectorAll("label").forEach((lb) => lb.classList.remove("right", "wrong"));
        sel.closest("label").classList.add(r.correct ? "right" : "wrong");
        fb(status, r.correct, r.correct ? "Correct" : "Not this one");
        out.replaceChildren(solutionBox((r.why_not ? `<p><strong>That answer comes from:</strong> ${r.why_not}.</p>` : "") + (r.correct ? r.solution : "<p>Try another choice, or read on.</p>" + r.solution)));
      });
      card.append(ul, h("div", { class: "row" }, btn, status, it.calc ? desmosButton(card) : null), out);
      typeset(card); mcqs.append(card, h("div", { style: "height:14px" }));
    });
    wrap.append(mcqs);
    if (L.frq.length) {   // some topics have no AP-style free-response question
      wrap.append(h("h2", { style: "margin-top:28px" }, "Free response"),
        h("p", { class: "muted" }, "Write full solutions on paper, as on the exam. Enter final answers to check them, then score yourself with the AP-style scoring guide."));
      frqSection(L.frq, wrap);
    }
    app.append(wrap);
  }

  function frqSection(frqs, wrap, locked = false) {
    frqs.forEach((f) => {
      const card = h("div", { class: "card" }, h("div", { class: "tag" }, f.title, h("span", { class: "calc" }, f.calc ? "calculator allowed" : "no calculator"),
        h("span", { class: "muted", style: "font-weight:400" }, `${f.points} points · ${f.type}`)), h("div", { html: f.html }), figureEl(f.figure));
      let earned = 0; const total = h("strong");
      const upd = () => { total.textContent = `${earned} / ${f.points}`; };
      f.parts.forEach((p) => {
        const part = answerCard({ id: p.id, html: `<strong>(${p.label})</strong> ` + p.html, answer_kind: p.answer_kind, units: p.units }, { area: "frq", cls: "block" });
        const rub = h("div");
        const btn = h("button", { class: "btn small", type: "button" }, "Score yourself");
        btn.addEventListener("click", async () => {
          btn.hidden = true;
          const r = await post(app.dataset.check, { item: p.id, given: "", reveal: true, area: "frq" });
          const ul = h("ul", { class: "rubric" });
          let mine = S.frq[p.id] ?? 0;
          r.rubric.forEach((line, k) => {
            const cb = h("input", { type: "checkbox" });
            if (k < mine) cb.checked = true;
            cb.addEventListener("change", async () => {
              const got = [...ul.querySelectorAll("input")].reduce((s, c, j) => s + (c.checked ? r.rubric[j].points : 0), 0);
              earned += got - mine; mine = got; upd();
              await post(app.dataset.frq, { part: p.id, earned: got });
            });
            ul.append(h("li", {}, cb, h("span", { class: "pts" }, `${line.points} pt`), h("span", { html: line.html })));
          });
          rub.append(h("div", { class: "solution" }, h("div", { class: "lbl" }, "Scoring guide: check each point you earned"), ul));
          typeset(rub);
        });
        earned += S.frq[p.id] ?? 0;
        if (locked) btn.hidden = true;             // class students score themselves after the teacher releases results
        part.append(h("div", { class: "row" }, btn), rub);
        card.append(part);
      });
      upd();
      if (!locked) card.append(h("p", { style: "text-align:right" }, "Your score: ", total));
      typeset(card); wrap.append(card);
    });
  }

  // quiz(): graded on submit. unittest reuses it with Part A / Part B headings, then adds the FRQs.
  function unittest() {
    const A = S.assess || { mode: "individual" };
    const nA = L.quiz.filter((q) => q.part === "A").length, nB = L.quiz.length - nA;
    const fA = L.frq.filter((f) => !f.calc), fB = L.frq.filter((f) => f.calc);
    const locked = A.mode === "class" && !A.released;
    if (S.print && A.mode !== "class") app.append(printCard(S.print));
    quiz({ what: "test",
      intro: `Part 1, no calculator: ${nA} multiple choice${fA.length ? ` and ${fA.length} free response` : ""}. `
        + `Part 2, calculator allowed: ${nB} multiple choice${fB.length ? ` and ${fB.length} free response` : ""}.`
        + (A.mode === "class" ? "" : " Multiple choice is graded when you submit; score the free response yourself with the rubric."),
      split: ({ p1, p2 }) => {
        const frqHead = (part) => h("h3", { style: "margin-top:24px" }, `Free response, ${part}`);
        const note = h("p", { class: "muted" }, locked
          ? "Write full solutions on paper and enter your final answers. They're saved for your teacher."
          : "Write full solutions on paper. Enter final answers to check them, then score yourself.");
        if (fA.length) { const box = h("div"); p1.append(frqHead("no calculator"), note, box); frqSection(fA, box, locked); }
        if (fB.length) {
          const box = h("div");
          const items = p2.querySelector(".items");
          items.after(frqHead("calculator allowed"), note.cloneNode(true), box);
          frqSection(fB, box, locked);
        }
      } });
  }

  // a docked graphing calculator for calculator sections (Desmos, like the AP exam's Bluebook)
  function calculatorDock() {
    if (document.querySelector(".desmos-dock")) return;
    const box = h("div", { class: "desmos-host" });
    const toggle = h("button", { class: "btn small", type: "button" }, "Hide calculator");
    const dock = h("aside", { class: "desmos-dock", "aria-label": "Graphing calculator" }, h("div", { class: "row" }, h("strong", {}, "Calculator"), toggle), box);
    toggle.addEventListener("click", () => {
      const off = dock.classList.toggle("min");
      document.body.classList.toggle("has-dock", !off);
      toggle.textContent = off ? "Show calculator" : "Hide calculator";
    });
    document.body.append(dock);
    document.body.classList.add("has-dock");
    if (window.Desmos) window.Desmos.GraphingCalculator(box, { invertedColors: document.documentElement.dataset.theme === "slate" });
    else box.append(h("p", { class: "muted", style: "padding:12px" }, "The graphing calculator could not load."));
  }

  // solo students can take the test on paper and check it against the solutions manual
  function printCard(pr) {
    const links = pr.forms.flatMap((f) => [
      h("a", { class: "btn small", href: f.test, target: "_blank", rel: "noopener" }, `Form ${f.form} (print)`),
      h("a", { class: "btn small", href: f.key, target: "_blank", rel: "noopener" }, `Form ${f.form} solutions manual`)]);
    return h("details", { class: "card print-test" }, h("summary", {}, "Prefer paper? Print the test instead"),
      h("p", {}, "Print a form, take it with a timer (no calculator for Part 1), then check your work against its solutions manual."),
      h("div", { class: "row" }, ...links));
  }

  const start = () => ({ notes, practice, quiz: () => quiz(), testprep, unittest })[area]();
  // KaTeX and MathLive load with defer; wait for both before rendering.
  const ready = () => window.renderMathInElement && window.customElements.get("math-field");
  if (ready()) start();
  else {
    const t0 = Date.now();
    const t = setInterval(() => {
      // after 6 s start anyway: plain inputs still work if the math keyboard never loads
      if (ready() || (window.renderMathInElement && Date.now() - t0 > 6000)) { clearInterval(t); start(); }
    }, 30);
  }
})();
