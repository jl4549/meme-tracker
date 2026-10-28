// Switch between the three views of the meme trace. Include right after <body> in each page:
//   <script src="nav.js"></script>
// Uses each page's own color tokens (--ink, --bg, --line, --muted), so it matches light and dark mode.
(() => {
  const VIEWS = [
    ["demo.html", "Story", "27 versions, step by step · RQ1 + RQ2"],
    ["lenses.html", "Timeline", "when each change happens · RQ1–RQ3"],
    ["chain_viewer.html", "All quotes", "every quote post on one map"],
  ];
  const here = location.pathname.split("/").pop() || "demo.html";
  const css = document.createElement("style");
  css.textContent = `
    .viewnav { display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 6px 14px; padding: 10px 16px;
      background: var(--bg); border-bottom: 1px solid var(--line); font: 14px/1.3 system-ui, -apple-system, "Segoe UI", sans-serif; }
    .viewnav .seg { display: inline-flex; border: 1px solid var(--line); border-radius: 99px; padding: 3px; background: var(--paper, var(--panel, transparent)); }
    .viewnav a { padding: 5px 14px; border-radius: 99px; color: var(--ink); text-decoration: none; white-space: nowrap; }
    .viewnav a:hover { background: var(--line); }
    .viewnav a[aria-current="page"] { background: var(--ink); color: var(--bg); }
    .viewnav .what { color: var(--muted); font-size: 13px; }
    @media (max-width: 520px) { .viewnav a { padding: 5px 10px; } .viewnav .what { width: 100%; text-align: center; } }`;
  document.head.appendChild(css);
  const cur = VIEWS.find(([f]) => f === here);
  const nav = document.createElement("nav");
  nav.className = "viewnav";
  nav.setAttribute("aria-label", "Views");
  nav.innerHTML = `<div class="seg">${VIEWS.map(([f, label, what]) =>
    `<a href="${f}" title="${what}"${f === here ? ' aria-current="page"' : ""}>${label}</a>`).join("")}</div>
    ${cur ? `<span class="what">${cur[2]}</span>` : ""}`;
  document.body.prepend(nav);
})();
