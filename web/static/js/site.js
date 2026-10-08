// Every page: typeset inline $...$ math in .mathy elements once KaTeX's auto-render has loaded.
// (Was an onload= attribute; the Content-Security-Policy allows no inline handlers.)
(function () {
  if (!window.renderMathInElement) return;
  document.querySelectorAll(".mathy").forEach((e) => window.renderMathInElement(e, {
    throwOnError: false, delimiters: [{ left: "$", right: "$", display: false }] }));
})();
