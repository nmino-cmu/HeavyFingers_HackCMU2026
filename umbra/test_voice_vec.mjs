import { voiceVec } from "./web/voice-vec.js";

function tone(hz, sec, rate) {
  const n = Math.floor(sec * rate);
  const x = new Float32Array(n);
  for (let i = 0; i < n; i++) x[i] = 0.25 * Math.sin((2 * Math.PI * hz * i) / rate);
  return x;
}

function l2(a, b) {
  let s = 0;
  for (let i = 0; i < 16; i++) {
    const d = a[i] - b[i];
    s += d * d;
  }
  return s;
}

const rate = 48000;
const t0 = Date.now();
const a = voiceVec(tone(220, 12, rate), rate);
const ms = Date.now() - t0;
if (ms > 2000) throw new Error("enroll voiceVec too slow: " + ms + "ms");
const b = voiceVec(tone(220, 12, rate), rate);
const c = voiceVec(tone(880, 12, rate), rate);
if (a.length !== 4096) throw new Error("need 4096 slots");
if (l2(a, b) > 1e-8) throw new Error("not stable " + l2(a, b));
if (!(l2(a, c) > 1e-4)) throw new Error("tones not separated " + l2(a, c));
console.log("voiceVec ok", ms + "ms", "sep", l2(a, c).toFixed(4));
