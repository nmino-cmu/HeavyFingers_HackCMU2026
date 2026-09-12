/* Desktop windows + tiled logo background. Positions persist locally. */
(function (g) {
  const LOGO = "/assets/logo.png";
  const TILE_W = 94;
  const TILE_H = 43;
  const EDGES = ["n", "s", "e", "w", "ne", "nw", "se", "sw"];
  let zTop = 20;
  let grain = null;

  function injectFilter() {
    if (document.getElementById("umbra-chroma")) return;
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("width", "0");
    svg.setAttribute("height", "0");
    svg.setAttribute("aria-hidden", "true");
    svg.style.position = "absolute";
    svg.innerHTML =
      '<filter id="umbra-chroma" x="-20%" y="-20%" width="140%" height="140%">' +
      '<feOffset in="SourceGraphic" dx="-2.2" dy="0" result="r"/>' +
      '<feColorMatrix in="r" type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.85 0" result="r2"/>' +
      '<feOffset in="SourceGraphic" dx="2.2" dy="0.4" result="c"/>' +
      '<feColorMatrix in="c" type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.75 0" result="c2"/>' +
      '<feBlend in="r2" in2="c2" mode="screen" result="split"/>' +
      '<feBlend in="split" in2="SourceGraphic" mode="screen"/>' +
      "</filter>";
    document.body.prepend(svg);
  }

  function paintBg(host, mode) {
    if (!host) return;
    injectFilter();
    host.querySelectorAll(".bg-tile").forEach((n) => n.remove());
    host.classList.add("bg-aberration", mode === "face" ? "bg-face" : "bg-subtle");
    const vw = Math.max(host.clientWidth, window.innerWidth);
    const vh = Math.max(host.clientHeight, window.innerHeight);
    const gapX = mode === "face" ? 28 : 48;
    const gapY = mode === "face" ? 18 : 36;
    const cols = Math.ceil(vw / (TILE_W + gapX)) + 2;
    const rows = Math.ceil(vh / (TILE_H + gapY)) + 2;
    for (let y = 0; y < rows; y++) {
      for (let x = 0; x < cols; x++) {
        const img = document.createElement("img");
        img.src = LOGO;
        img.alt = "";
        img.width = TILE_W;
        img.height = TILE_H;
        img.className = "bg-tile";
        img.style.width = TILE_W + "px";
        img.style.height = TILE_H + "px";
        img.style.left = x * (TILE_W + gapX) - TILE_W + "px";
        img.style.top = y * (TILE_H + gapY) - TILE_H + "px";
        img.style.animationDelay = ((x + y) * 0.35) + "s";
        host.appendChild(img);
      }
    }
    if (g.UmbraGrain) {
      if (grain && grain.destroy) grain.destroy();
      grain = g.UmbraGrain.mount(host, { opacity: mode === "face" ? 0.28 : 0.16, interval: 220 });
    }
  }

  function storeKey(id) { return "umbra.win.v3." + id; }

  function deskOf(el) {
    return el.closest(".desk") || el.offsetParent || document.body;
  }

  function save(el) {
    const id = el.dataset.win;
    if (!id) return;
    localStorage.setItem(storeKey(id), JSON.stringify({
      x: parseFloat(el.style.left) || 0,
      y: parseFloat(el.style.top) || 0,
      w: el.offsetWidth,
      h: el.offsetHeight,
      min: el.classList.contains("is-min"),
      z: el.style.zIndex || 10,
    }));
  }

  function restore(el) {
    const id = el.dataset.win;
    if (!id) return false;
    let s;
    try { s = JSON.parse(localStorage.getItem(storeKey(id)) || "null"); } catch (e) { s = null; }
    if (!s) return false;
    el.style.left = s.x + "px";
    el.style.top = s.y + "px";
    if (s.w) el.style.width = s.w + "px";
    if (s.h && !s.min) el.style.height = s.h + "px";
    if (s.z) { el.style.zIndex = s.z; zTop = Math.max(zTop, Number(s.z) || 20); }
    if (s.min) el.classList.add("is-min");
    const desk = deskOf(el);
    const pad = 20;
    if (s.w > desk.clientWidth - pad || s.h > desk.clientHeight - pad) return false;
    return true;
  }

  function fitBox(dw, dh, rw, rh, pad, capOne) {
    const maxW = Math.max(240, dw - pad * 2);
    const maxH = Math.max(140, dh - pad * 2);
    let s = Math.min(maxW / rw, maxH / rh);
    if (capOne !== false) s = Math.min(1, s);
    const w = Math.round(rw * s);
    const h = Math.round(rh * s);
    return { w, h, x: Math.round((dw - w) / 2), y: Math.round((dh - h) / 2) };
  }

  function applyBox(el, box) {
    el.style.left = box.x + "px";
    el.style.top = box.y + "px";
    el.style.width = box.w + "px";
    el.style.height = box.h + "px";
  }

  function placeLaunch(el) {
    const desk = deskOf(el);
    const dw = desk.clientWidth || 960;
    const dh = desk.clientHeight || 640;
    const pad = 40;
    const preset = el.getAttribute("data-win-preset") || "";
    if (preset === "face") {
      // Figma 1280×766 aspect; fill the desk with a modest inset so it launches larger
      // than the artboard pixel size while keeping the same window ratio.
      applyBox(el, fitBox(dw, dh, 1280, 766, 28, false));
      return;
    }
    if (preset === "welcome") {
      applyBox(el, { x: pad, y: pad, w: Math.min(460, dw - pad * 2), h: Math.min(480, dh - pad * 2) });
      return;
    }
    if (preset === "note") {
      applyBox(el, { x: pad, y: Math.min(dh - 200, pad + 500), w: Math.min(460, dw - pad * 2), h: 200 });
      return;
    }
    if (preset === "lab") {
      const w = Math.min(730, dw - pad * 2);
      const h = Math.min(760, dh - pad * 2);
      applyBox(el, { x: Math.max(pad, dw - w - pad), y: pad, w, h });
      return;
    }
    if (preset === "messages") {
      applyBox(el, { x: pad, y: pad, w: Math.min(420, dw - pad * 2), h: Math.min(460, dh - pad * 2) });
      return;
    }
    if (preset === "panel") {
      applyBox(el, fitBox(dw, dh, 540, 400, pad + 40));
      return;
    }
    const w = Math.min(el.offsetWidth || 400, dw - pad * 2);
    const h = Math.min(el.offsetHeight || 320, dh - pad * 2);
    applyBox(el, { x: pad, y: pad, w, h });
  }

  function raise(el) {
    zTop += 1;
    el.style.zIndex = String(zTop);
    save(el);
  }

  function addEdges(el) {
    if (el.querySelector(".win-edge")) return;
    EDGES.forEach((dir) => {
      const h = document.createElement("div");
      h.className = "win-edge win-edge-" + dir;
      h.dataset.dir = dir;
      h.setAttribute("aria-hidden", "true");
      el.appendChild(h);
    });
  }

  function bindResize(el, handle, dir) {
    handle.addEventListener("pointerdown", (ev) => {
      ev.preventDefault();
      ev.stopPropagation();
      raise(el);
      el.classList.remove("is-min");
      const startX = ev.clientX, startY = ev.clientY;
      const startL = el.offsetLeft, startT = el.offsetTop;
      const startW = el.offsetWidth, startH = el.offsetHeight;
      const desk = deskOf(el);
      const minW = 240, minH = 140;
      handle.setPointerCapture(ev.pointerId);
      function move(e) {
        const dx = e.clientX - startX, dy = e.clientY - startY;
        let l = startL, t = startT, w = startW, h = startH;
        if (dir.indexOf("e") >= 0) w = Math.max(minW, startW + dx);
        if (dir.indexOf("s") >= 0) h = Math.max(minH, startH + dy);
        if (dir.indexOf("w") >= 0) {
          w = Math.max(minW, startW - dx);
          l = startL + (startW - w);
        }
        if (dir.indexOf("n") >= 0) {
          h = Math.max(minH, startH - dy);
          t = startT + (startH - h);
        }
        l = Math.min(Math.max(-40, l), desk.clientWidth - 80);
        t = Math.min(Math.max(-8, t), desk.clientHeight - 40);
        el.style.left = l + "px";
        el.style.top = t + "px";
        el.style.width = w + "px";
        el.style.height = h + "px";
      }
      function up() {
        handle.removeEventListener("pointermove", move);
        handle.removeEventListener("pointerup", up);
        save(el);
      }
      handle.addEventListener("pointermove", move);
      handle.addEventListener("pointerup", up);
    });
  }

  function bind(el) {
    const bar = el.querySelector(".win-bar");
    const minBtn = el.querySelector("[data-win-min]");
    const closeBtn = el.querySelector("[data-win-close]");
    addEdges(el);
    placeLaunch(el);
    el.addEventListener("pointerdown", () => raise(el));

    if (bar) {
      bar.addEventListener("pointerdown", (ev) => {
        if (ev.target.closest("button, a, .win-edge")) return;
        raise(el);
        const r = el.getBoundingClientRect();
        const desk = deskOf(el);
        const ox = ev.clientX - r.left;
        const oy = ev.clientY - r.top;
        bar.setPointerCapture(ev.pointerId);
        function move(e) {
          const dr = desk.getBoundingClientRect();
          const l = e.clientX - dr.left - ox;
          const t = e.clientY - dr.top - oy;
          el.style.left = Math.min(Math.max(-el.offsetWidth + 80, l), desk.clientWidth - 40) + "px";
          el.style.top = Math.min(Math.max(0, t), desk.clientHeight - 28) + "px";
        }
        function up() {
          bar.removeEventListener("pointermove", move);
          bar.removeEventListener("pointerup", up);
          save(el);
        }
        bar.addEventListener("pointermove", move);
        bar.addEventListener("pointerup", up);
      });
    }

    el.querySelectorAll(".win-edge").forEach((h) => bindResize(el, h, h.dataset.dir));
    const grip = el.querySelector(".win-resize");
    if (grip) bindResize(el, grip, "se");

    if (minBtn) {
      minBtn.addEventListener("click", () => {
        el.classList.toggle("is-min");
        save(el);
      });
    }
    if (closeBtn) {
      closeBtn.addEventListener("click", () => {
        el.hidden = true;
        save(el);
      });
    }
  }

  function openWin(id) {
    const el = document.querySelector('[data-win="' + id + '"]');
    if (!el) return;
    el.hidden = false;
    el.classList.remove("is-min");
    raise(el);
  }

  function boot() {
    const bg = document.querySelector("[data-umbra-bg]");
    paintBg(bg, document.body.getAttribute("data-bg") || "subtle");
    window.addEventListener("resize", () => {
      paintBg(bg, document.body.getAttribute("data-bg") || "subtle");
    });
    document.querySelectorAll("[data-win]").forEach(bind);
    document.querySelectorAll("[data-open-win]").forEach((btn) => {
      btn.addEventListener("click", () => openWin(btn.getAttribute("data-open-win")));
    });
  }

  g.UmbraWindows = { boot, openWin, paintBg };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})(typeof window !== "undefined" ? window : globalThis);
