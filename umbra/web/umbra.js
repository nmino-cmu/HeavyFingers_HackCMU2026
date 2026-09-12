/* Drop-in: card + fixture AND. Crops and sk stay on this browser. */
(function (g) {
  let localP;
  function local() {
    localP = localP || import("./fhe-local.js");
    return localP;
  }
  async function j(url, opt) {
    const r = await fetch(url, opt);
    if (!r.ok) throw new Error(await r.text());
    return r.json();
  }
  const SESS = "umbra.session";
  g.Umbra = {
    card: () => local().then((m) => m.card()),
    sample: () => Promise.resolve({}),
    samples: () => Promise.resolve({ samples: [] }),
    fixture: () => Promise.resolve({}),
    roster: () => local().then((m) => m.roster()),
    hop: () => Promise.resolve({}),
    last: () => Promise.resolve({}),
    cutout: () => Promise.resolve({}),
    escrows: () => Promise.resolve({ escrows: [], last_hop: {} }),
    receipts: () => Promise.resolve({ receipts: [] }),
    enroll: (fd) => local().then((m) => m.enroll(fd)),
    verify: (fd) => local().then((m) => m.verify(fd)),
    session: {
      get() {
        try { return JSON.parse(localStorage.getItem(SESS) || "null"); } catch (e) { return null; }
      },
      set(obj) {
        localStorage.setItem(SESS, JSON.stringify(obj || {}));
      },
      clear() { localStorage.removeItem(SESS); },
    },
    // Stable desk nym. Never show a roster id. Seed stays in localStorage.
    async veil() {
      const sess = (g.Umbra.session.get() || {});
      if (sess.veil && /^veil-[0-9a-f]{8}$/.test(sess.veil)) return sess.veil;
      const seed = sess.id || (crypto.randomUUID && crypto.randomUUID()) || String(Date.now());
      const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode("umbra-veil-v1" + seed));
      const hex = [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
      sess.veil = "veil-" + hex.slice(0, 8);
      g.Umbra.session.set(sess);
      return sess.veil;
    },
    inbox: {
      _box: "umbra.inbox.v1",
      _k: "umbra.seal.v1",
      async _key() {
        let raw = localStorage.getItem(g.Umbra.inbox._k);
        if (!raw) {
          const k = await crypto.subtle.generateKey({ name: "AES-GCM", length: 256 }, true, ["encrypt", "decrypt"]);
          const exp = await crypto.subtle.exportKey("raw", k);
          raw = btoa(String.fromCharCode.apply(null, [...new Uint8Array(exp)]));
          localStorage.setItem(g.Umbra.inbox._k, raw);
          return k;
        }
        const bytes = Uint8Array.from(atob(raw), (c) => c.charCodeAt(0));
        return crypto.subtle.importKey("raw", bytes, "AES-GCM", false, ["encrypt", "decrypt"]);
      },
      load() {
        try { return JSON.parse(localStorage.getItem(g.Umbra.inbox._box) || "[]"); } catch (e) { return []; }
      },
      async seal(handle, text) {
        const k = await g.Umbra.inbox._key();
        const iv = crypto.getRandomValues(new Uint8Array(12));
        const ct = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, k, new TextEncoder().encode(String(text || "")));
        const row = {
          handle: String(handle || "nym").slice(0, 32),
          iv: btoa(String.fromCharCode.apply(null, [...iv])),
          ct: btoa(String.fromCharCode.apply(null, [...new Uint8Array(ct)])),
          t: Date.now(),
        };
        const all = g.Umbra.inbox.load();
        all.unshift(row);
        localStorage.setItem(g.Umbra.inbox._box, JSON.stringify(all.slice(0, 32)));
        return row;
      },
      async open(row) {
        const k = await g.Umbra.inbox._key();
        const iv = Uint8Array.from(atob(row.iv), (c) => c.charCodeAt(0));
        const ct = Uint8Array.from(atob(row.ct), (c) => c.charCodeAt(0));
        const raw = await crypto.subtle.decrypt({ name: "AES-GCM", iv }, k, ct);
        return new TextDecoder().decode(raw);
      },
    },
    qaFace: (blob, pose) => local().then((m) => m.qaFace(blob, pose)),
    qaVoice: (blob) => local().then((m) => m.qaVoice(blob)),
    openCam: async (video, opt) => {
      if (!window.isSecureContext || !navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error("Camera is blocked on this URL. Use HTTPS.");
      }
      const videoOpt = (opt && opt.video) || { width: { ideal: 1280 }, height: { ideal: 720 } };
      const wantAudio = !!(opt && opt.audio);
      let stream;
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: videoOpt, audio: wantAudio });
      } catch (e) {
        stream = await navigator.mediaDevices.getUserMedia({ video: videoOpt, audio: !wantAudio }).catch(() => { throw e; });
      }
      video.muted = true;
      video.playsInline = true;
      video.hidden = false;
      video.srcObject = new MediaStream(stream.getVideoTracks());
      try { await video.play(); } catch (e) {}
      return stream;
    },
    withMic: async (stream) => {
      try {
        const mic = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
        mic.getAudioTracks().forEach((t) => stream.addTrack(t));
      } catch (e) {}
      return stream;
    },
    grabCover: (v) => {
      if (!v || !v.videoWidth || !v.videoHeight) return Promise.resolve(null);
      const vw = v.videoWidth, vh = v.videoHeight;
      const cw = v.clientWidth || vw, ch = v.clientHeight || vh;
      const scale = Math.max(cw / vw, ch / vh);
      let sw = Math.min(vw, cw / scale), sh = Math.min(vh, ch / scale);
      // hidden/mid-layout element gives a sliver (or NaN): fall back to the full frame, never a 0×0 canvas
      if (!(sw >= 8 && sh >= 8)) { sw = vw; sh = vh; }
      const c = document.createElement("canvas");
      c.width = Math.round(sw);
      c.height = Math.round(sh);
      c.getContext("2d").drawImage(v, (vw - sw) / 2, (vh - sh) / 2, sw, sh, 0, 0, c.width, c.height);
      return new Promise((res) => c.toBlob(res, "image/jpeg", 0.92));
    },
    // Full sensor frame — same pixels ffmpeg sees on a recorded take. Use this for enroll templates.
    grabFrame: (v) => {
      if (!v || !v.videoWidth || !v.videoHeight) return Promise.resolve(null);
      const c = document.createElement("canvas");
      c.width = v.videoWidth;
      c.height = v.videoHeight;
      c.getContext("2d").drawImage(v, 0, 0);
      return new Promise((res) => c.toBlob(res, "image/jpeg", 0.92));
    },
    sealViz: (root, on, ms, after) => {
      if (!root) return;
      const glyphs = "01ABCDEF89";
      const rows = root.querySelectorAll(".ut-cipher");
      if (root._off) { clearTimeout(root._off); root._off = 0; }
      root._after = on ? after : null;
      if (on) {
        rows.forEach((row, r) => {
          if (row.childElementCount) return;
          for (let i = 0; i < 16; i++) {
            const s = document.createElement("span");
            s.textContent = glyphs[(i * 7 + r * 3) % glyphs.length];
            row.appendChild(s);
          }
        });
      }
      root.classList.toggle("is-on", !!on);
      if (!on) {
        if (root._t) clearInterval(root._t);
        root._t = 0;
        return;
      }
      if (!root._t) {
        root._n = 0;
        root._t = setInterval(() => {
          const probe = rows[0], rost = rows[1], ev = rows[2];
          const flick = (row) => {
            if (!row || !row.children.length) return;
            const n = row.children[(Math.random() * row.children.length) | 0];
            n.textContent = glyphs[(Math.random() * glyphs.length) | 0];
            n.classList.toggle("on");
          };
          flick(probe);
          flick(rost);
          if (probe && rost && ev) {
            // CKKS add: eval stays ciphertext. Rotate now and then, like a slot rotate.
            if ((root._n++ % 8) === 0 && ev.firstChild) ev.appendChild(ev.firstChild);
            const n = Math.min(probe.children.length, rost.children.length, ev.children.length);
            for (let i = 0; i < n; i++) {
              const a = glyphs.indexOf(probe.children[i].textContent);
              const b = glyphs.indexOf(rost.children[i].textContent);
              ev.children[i].textContent = glyphs[(((a < 0 ? 0 : a) + (b < 0 ? 0 : b)) % glyphs.length)];
              ev.children[i].classList.toggle("on", probe.children[i].classList.contains("on") !== rost.children[i].classList.contains("on"));
            }
          } else {
            flick(probe);
          }
        }, 120);
      }
      if (ms > 0) root._off = setTimeout(() => {
        const next = root._after;
        root._after = null;
        g.Umbra.sealViz(root, false);
        if (next) next();
      }, ms);
    },
    loadEta: () => {
      const base = { face: 19000, voice: 3500, words: 4500, wave: 19000 };
      try { return Object.assign(base, JSON.parse(localStorage.getItem("umbra.laneEta") || "{}")); }
      catch (e) { return base; }
    },
    saveEta: (ms) => {
      if (!ms) return;
      const cur = g.Umbra.loadEta();
      const next = {};
      ["face", "voice", "words", "wave"].forEach((k) => {
        if (ms[k] > 200) next[k] = Math.round(cur[k] * 0.4 + ms[k] * 0.6);
      });
      if (Object.keys(next).length) localStorage.setItem("umbra.laneEta", JSON.stringify(Object.assign(cur, next)));
    },
    paintLanes: (box, opt) => {
      if (!box) return;
      opt = opt || {};
      const items = opt.items || [];
      const mode = opt.mode || "idle";
      const bits = opt.bits || [];
      if (box._raf) cancelAnimationFrame(box._raf);
      box._raf = 0;
      box.className = "lights" + (mode === "run" ? " busy" : "");
      box.innerHTML = "";
      items.forEach((it, i) => {
        const row = document.createElement("div");
        const done = mode === "done";
        const ok = done && (it.ok === true || bits[i] === 1);
        const no = done && (it.ok === false || bits[i] === 0);
        row.className = "lane" + (mode === "run" ? " is-run" : "") + (ok ? " is-on" : "") + (no ? " is-off" : "");
        const bit = document.createElement("div");
        bit.className = "bit";
        bit.textContent = it.label || "";
        bit.title = it.id || "";
        row.appendChild(bit);
        if (mode !== "idle") {
          const track = document.createElement("div");
          track.className = "lane-track";
          const fill = document.createElement("i");
          fill.style.width = done ? "100%" : "0%";
          track.appendChild(fill);
          row.appendChild(track);
          const name = document.createElement("span");
          name.className = "lane-name";
          name.textContent = it.name || it.id || "";
          row.appendChild(name);
        }
        box.appendChild(row);
      });
      if (mode !== "run") return;
      const t0 = Date.now();
      const tick = () => {
        const rows = box.querySelectorAll(".lane");
        items.forEach((it, i) => {
          const eta = Math.max(400, it.eta || 4000);
          // ponytail: estimated fill, hold at 92% until /verify returns; stream ticks if we add them
          const pct = Math.min(0.92, (Date.now() - t0) / eta);
          const fill = rows[i] && rows[i].querySelector("i");
          if (fill) fill.style.width = (pct * 100).toFixed(1) + "%";
        });
        box._raf = requestAnimationFrame(tick);
      };
      box._raf = requestAnimationFrame(tick);
    },
  };
})(typeof window !== "undefined" ? window : globalThis);
