/* Drop-in: card + fixture AND. Crops and sk stay on the host that serves this. */
(function (g) {
  async function j(url, opt) {
    const r = await fetch(url, opt);
    if (!r.ok) throw new Error(await r.text());
    return r.json();
  }
  g.Umbra = {
    card: () => j("/card"),
    sample: (lane) => j("/sample", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ lane }) }),
    fixture: () => j("/fixture", { method: "POST" }),
    roster: () => j("/roster"),
    enroll: (fd) => j("/enroll", { method: "POST", body: fd }),
    verify: (fd) => j("/verify", { method: "POST", body: fd }),
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
    // JPEG of what the user sees (object-fit: cover crop). Null only before the first frame arrives.
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
  };
})(typeof window !== "undefined" ? window : globalThis);
