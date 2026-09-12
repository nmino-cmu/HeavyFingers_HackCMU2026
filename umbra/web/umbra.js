/* Drop-in: card + fixture AND. Crops and sk stay on the host that serves this. */
(function (g) {
  async function j(url, opt) {
    const r = await fetch(url, opt);
    if (!r.ok) throw new Error(await r.text());
    return r.json();
  }
  const SESS = "umbra.session";
  g.Umbra = {
    card: () => j("/card"),
    sample: (lane) => j("/sample", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ lane }) }),
    samples: () => j("/samples"),
    fixture: () => j("/fixture", { method: "POST" }),
    roster: () => j("/roster"),
    hop: () => j("/hop", { method: "POST" }),
    last: () => j("/last"),
    escrows: () => j("/escrows"),
    receipts: () => j("/receipts"),
    enroll: (fd) => j("/enroll", { method: "POST", body: fd }),
    verify: (fd) => j("/verify", { method: "POST", body: fd }),
    session: {
      get() {
        try { return JSON.parse(localStorage.getItem(SESS) || "null"); } catch (e) { return null; }
      },
      set(obj) {
        localStorage.setItem(SESS, JSON.stringify(obj || {}));
      },
      clear() { localStorage.removeItem(SESS); },
    },
    qaFace: (blob, pose) => {
      const fd = new FormData();
      fd.append("face", blob, "face.jpg");
      fd.append("pose", pose || "front");
      return j("/qa/face", { method: "POST", body: fd });
    },
    qaVoice: (blob) => {
      const fd = new FormData();
      fd.append("voice", blob, "voice.wav");
      return j("/qa/voice", { method: "POST", body: fd });
    },
    openCam: async (video, opt) => {
      if (!window.isSecureContext || !navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error("Camera is blocked on this URL. Use http://127.0.0.1:8765/");
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
  };
})(typeof window !== "undefined" ? window : globalThis);
