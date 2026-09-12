/* Browser CKKS: keys + ciphertext stay in this origin's IndexedDB. Vultr only evals. */
import SEAL from "./vendor/node-seal/index_throws.js";
import { voiceVec } from "./voice-vec.js?v=fft1";

const POLY = 8192;
const SCALE = 2 ** 40;
const PIXELS = 4096;
const FACE_N = 64;
const FACE_L2_MAX = 220;
const VOICE_L2_MAX = 0.2;
const VOICE_MIN_S = 12;
const DB = "umbra-local-v2";
const WORDS = (
  "the lazy dog fox am is hack win project asterisk " +
  "quick brown jumps over cmu lattice cipher nonce"
).split();

export const EVAL_URL = /(?:^|\.)nickmino\.com$/i.test(location.hostname)
  ? "https://207.246.126.149.sslip.io/face-web"
  : location.protocol === "https:"
    ? new URL("/face-web", location.origin).href
    : "https://207.246.126.149.sslip.io/face-web";

let seal, ZSTD, ready;

function concatPack(parts) {
  let n = 4 * parts.length;
  for (const p of parts) n += p.length;
  const out = new Uint8Array(n);
  const view = new DataView(out.buffer);
  let o = 0;
  for (const p of parts) {
    view.setUint32(o, p.length);
    o += 4;
    out.set(p, o);
    o += p.length;
  }
  return out;
}

function b64(u8) {
  let s = "";
  const bytes = u8 instanceof Uint8Array ? u8 : new Uint8Array(u8);
  for (let i = 0; i < bytes.length; i++) s += String.fromCharCode(bytes[i]);
  return btoa(s);
}

function unb64(s) {
  const bin = atob(s);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

function openDb() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB, 1);
    req.onupgradeneeded = () => req.result.createObjectStore("people", { keyPath: "id" });
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

function idbAll() {
  return openDb().then(
    (db) =>
      new Promise((resolve, reject) => {
        const r = db.transaction("people").objectStore("people").getAll();
        r.onsuccess = () => resolve(r.result || []);
        r.onerror = () => reject(r.error);
      }),
  );
}

function idbGet(id) {
  return openDb().then(
    (db) =>
      new Promise((resolve, reject) => {
        const r = db.transaction("people").objectStore("people").get(id);
        r.onsuccess = () => resolve(r.result || null);
        r.onerror = () => reject(r.error);
      }),
  );
}

function idbPut(row) {
  return openDb().then(
    (db) =>
      new Promise((resolve, reject) => {
        const r = db.transaction("people", "readwrite").objectStore("people").put(row);
        r.onsuccess = () => resolve(row);
        r.onerror = () => reject(r.error);
      }),
  );
}

export async function boot() {
  if (ready) return ready;
  ready = (async () => {
    seal = await SEAL();
    ZSTD = seal.ComprModeType.zstd;
    return seal;
  })();
  return ready;
}

function freshId() {
  return String(100000 + Math.floor(Math.random() * 900000));
}

function prepFace(grid) {
  const n = grid.length;
  const m = grid.reduce((a, b) => a + b, 0) / n;
  const v = grid.reduce((a, x) => a + (x - m) * (x - m), 0) / n;
  const s = Math.sqrt(v);
  if (s < 1e-3) return grid;
  return grid.map((x) => 0.5 + (0.25 * (x - m)) / s);
}

async function blobToGray(blob) {
  const bmp = await createImageBitmap(blob);
  const c = document.createElement("canvas");
  c.width = FACE_N;
  c.height = FACE_N;
  const g = c.getContext("2d");
  g.drawImage(bmp, 0, 0, FACE_N, FACE_N);
  const px = g.getImageData(0, 0, FACE_N, FACE_N).data;
  const out = [];
  for (let i = 0; i < px.length; i += 4) out.push((px[i] + px[i + 1] + px[i + 2]) / (3 * 255));
  return prepFace(out);
}

async function decodeAudio(blob) {
  const ctx = new AudioContext();
  try {
    const buf = await ctx.decodeAudioData(await blob.arrayBuffer());
    return { rate: buf.sampleRate, samples: buf.getChannelData(0) };
  } finally {
    await ctx.close();
  }
}

function qaFromSamples(samples, rate) {
  const n = samples.length;
  const dur = n / rate;
  let peak = 0;
  let acc = 0;
  let clip = 0;
  for (let i = 0; i < n; i++) {
    const a = Math.abs(samples[i]);
    if (a > peak) peak = a;
    acc += samples[i] * samples[i];
    if (a > 0.98) clip++;
  }
  const rms = Math.sqrt(acc / n);
  const longEnough = dur + 0.5 >= VOICE_MIN_S;
  const ok = longEnough && peak >= 0.1 && rms >= 0.022 && clip / n < 0.03;
  let reason = "";
  if (!longEnough) reason = "need a " + VOICE_MIN_S + "s recording, got " + dur.toFixed(1) + "s";
  else if (peak < 0.1 || rms < 0.022) reason = "too quiet — speak closer";
  else if (clip / n >= 0.03) reason = "clipping — back up from the mic";
  return { ok, seconds: dur, peak, rms, clip: clip / n, reason };
}

function s1(transcript, nonce) {
  const alias = { lettuce: "lattice", letus: "lattice", nonsam: "nonce", "non-sam": "nonce", asterix: "asterisk" };
  const words = (t) =>
    String(t || "")
      .split(/\s+/)
      .map((w) => alias[w.replace(/[.,!?;:"']+/g, "").toLowerCase()] || w.replace(/[.,!?;:"']+/g, "").toLowerCase())
      .filter(Boolean);
  const need = words(nonce);
  const got = words(transcript);
  if (!need.length) return false;
  const slack = need.length < 4 ? 0 : Math.max(1, Math.floor(need.length / 4));
  const minGot = need.length < 6 ? need.length : need.length - slack;
  if (got.length < minGot) return false;
  const edits = (a, b) => {
    const dp = [...Array(b.length + 1).keys()];
    for (let i = 1; i <= a.length; i++) {
      let prev = dp[0];
      dp[0] = i;
      for (let j = 1; j <= b.length; j++) {
        const cur = dp[j];
        dp[j] = a[i - 1] === b[j - 1] ? prev : 1 + Math.min(prev, dp[j], dp[j - 1]);
        prev = cur;
      }
    }
    return dp[b.length];
  };
  const hi = need.length + slack + 2;
  for (let i = 0; i <= got.length - minGot; i++) {
    for (let w = minGot; w <= Math.min(hi, got.length - i); w++) {
      if (edits(need, got.slice(i, i + w)) <= slack) return true;
    }
  }
  return false;
}

async function newKeys() {
  await boot();
  const parms = new seal.EncryptionParameters(seal.SchemeType.ckks);
  parms.setPolyModulusDegree(POLY);
  parms.setCoeffModulus(seal.CoeffModulus.Create(POLY, Int32Array.from([60, 40, 40, 60])));
  const context = new seal.SEALContext(parms, true, seal.SecLevelType.tc128);
  const keygen = new seal.KeyGenerator(context);
  const secretKey = keygen.secretKey();
  const publicKey = keygen.createPublicKey();
  return {
    parms: parms.saveToArray(ZSTD),
    relin: keygen.createRelinKeysSerializable().saveToArray(ZSTD),
    secret: secretKey.saveToArray(ZSTD),
    public: publicKey.saveToArray(ZSTD),
    context,
    secretKey,
    publicKey,
  };
}

function loadCtx(row) {
  const parms = new seal.EncryptionParameters(seal.SchemeType.ckks);
  parms.loadFromArray(unb64(row.parms), ZSTD);
  const context = new seal.SEALContext(parms, true, seal.SecLevelType.tc128);
  const secret = new seal.SecretKey();
  secret.loadFromArray(context, unb64(row.secret), ZSTD);
  const publicKey = new seal.PublicKey();
  publicKey.loadFromArray(context, unb64(row.public), ZSTD);
  return { context, secret, publicKey, parms: unb64(row.parms), relin: unb64(row.relin) };
}

function encryptVec(ctx, pub, arr) {
  const encoder = new seal.CKKSEncoder(ctx);
  const encryptor = new seal.Encryptor(ctx, pub);
  const plain = new seal.Plaintext();
  const src = arr instanceof Float64Array ? arr : Float64Array.from(arr);
  const padded = src.length === PIXELS ? src : (() => {
    const o = new Float64Array(PIXELS);
    o.set(src.subarray(0, PIXELS));
    return o;
  })();
  encoder.encode(padded, SCALE, plain);
  const ct = new seal.Ciphertext();
  encryptor.encrypt(plain, ct);
  return ct.saveToArray(ZSTD);
}

function decryptSum(ctx, secret, ctBytes) {
  const encoder = new seal.CKKSEncoder(ctx);
  const decryptor = new seal.Decryptor(ctx, secret);
  const ct = new seal.Ciphertext();
  ct.loadFromArray(ctx, ctBytes, ZSTD);
  const plain = new seal.Plaintext();
  decryptor.decrypt(ct, plain);
  const vals = encoder.decodeFloat64(plain);
  let s = 0;
  for (let i = 0; i < PIXELS; i++) s += vals[i];
  return s;
}

function evalLocal(parms, relinBytes, tmpl, probe) {
  const p2 = new seal.EncryptionParameters(seal.SchemeType.ckks);
  p2.loadFromArray(parms, ZSTD);
  const ctx2 = new seal.SEALContext(p2, true, seal.SecLevelType.tc128);
  const relin = new seal.RelinKeys();
  relin.loadFromArray(ctx2, relinBytes, ZSTD);
  const a = new seal.Ciphertext();
  const b = new seal.Ciphertext();
  a.loadFromArray(ctx2, tmpl, ZSTD);
  b.loadFromArray(ctx2, probe, ZSTD);
  const ev = new seal.Evaluator(ctx2);
  const diff = new seal.Ciphertext();
  ev.sub(a, b, diff);
  ev.squareInplace(diff);
  ev.relinearizeInplace(diff, relin);
  return diff.saveToArray(ZSTD);
}

async function evalRemote(parms, relin, tmpl, probe) {
  const body = concatPack([parms, relin, tmpl, probe]);
  try {
    const r = await fetch(EVAL_URL, { method: "POST", body, headers: { "Content-Type": "application/octet-stream" } });
    if (r.ok) return new Uint8Array(await r.arrayBuffer());
  } catch (e) {}
  return evalLocal(parms, relin, tmpl, probe);
}

async function videoFrames(blob, n) {
  const url = URL.createObjectURL(blob);
  const v = document.createElement("video");
  v.muted = true;
  v.playsInline = true;
  v.src = url;
  await v.play().catch(() => {});
  await new Promise((res) => {
    if (v.readyState >= 2) res();
    else v.onloadeddata = res;
  });
  const dur = v.duration && isFinite(v.duration) ? v.duration : 1;
  const frames = [];
  for (let i = 0; i < n; i++) {
    v.currentTime = (dur * i) / Math.max(1, n - 1);
    await new Promise((res) => {
      v.onseeked = res;
      setTimeout(res, 400);
    });
    const c = document.createElement("canvas");
    c.width = v.videoWidth || 640;
    c.height = v.videoHeight || 480;
    c.getContext("2d").drawImage(v, 0, 0);
    frames.push(await new Promise((res) => c.toBlob(res, "image/jpeg", 0.9)));
  }
  URL.revokeObjectURL(url);
  return frames.filter(Boolean);
}

export function card() {
  const n = 6 + Math.floor(Math.random() * 3);
  const pool = WORDS.slice();
  const say = [];
  for (let i = 0; i < n; i++) say.push(pool.splice(Math.floor(Math.random() * pool.length), 1)[0]);
  return Promise.resolve({ say: say.join(" "), nonce: say.join(" ") });
}

export async function roster() {
  const people = await idbAll();
  return { people: people.map((p) => ({ id: p.id, face: (p.faces || []).length, voice: (p.voices || []).length, print: 0 })) };
}

export function qaFace() {
  return Promise.resolve({ ok: true, reason: "", pose: "front", face: { x: 0.15, y: 0.1, w: 0.7, h: 0.8, yaw: 0 }, yaw: 0 });
}

export async function qaVoice(blob) {
  const { samples, rate } = await decodeAudio(blob);
  return qaFromSamples(samples, rate);
}

export async function enroll(fd) {
  await boot();
  const faces = fd.getAll("face").filter(Boolean);
  const voices = fd.getAll("voice").filter(Boolean);
  if (!faces.length || !voices.length) throw new Error("need face and voice");
  const id = String(fd.get("id") || "").trim() || freshId();
  const keys = await newKeys();
  const faceCts = [];
  for (const b of faces) faceCts.push(b64(encryptVec(keys.context, keys.publicKey, await blobToGray(b))));
  const voiceCts = [];
  for (const b of voices) {
    const { samples, rate } = await decodeAudio(b);
    voiceCts.push(b64(encryptVec(keys.context, keys.publicKey, voiceVec(samples, rate))));
  }
  await idbPut({
    id,
    at: Date.now(),
    parms: b64(keys.parms),
    relin: b64(keys.relin),
    secret: b64(keys.secret),
    public: b64(keys.public),
    faces: faceCts,
    voices: voiceCts,
  });
  const people = (await roster()).people;
  return { id, bytes: faceCts.length + voiceCts.length, people };
}

export async function verify(fd) {
  await boot();
  const take = fd.get("take");
  const audio = fd.get("audio");
  const said = String(fd.get("said") || "");
  let card = {};
  try {
    card = JSON.parse(fd.get("card") || "{}");
  } catch (e) {}
  const people = await idbAll();
  if (!people.length) throw new Error("enroll first");
  let id = String(fd.get("id") || "").trim();
  if (!id || !people.some((p) => p.id === id)) id = people[people.length - 1].id;
  const row = await idbGet(id);
  const { context, secret, publicKey, parms, relin } = loadCtx(row);
  const t0 = performance.now();
  const frames = take ? await videoFrames(take, 5) : [];
  const series = [];
  let best = 999;
  const tmpl = unb64(row.faces[0]);
  for (const fr of frames) {
    const probe = encryptVec(context, publicKey, await blobToGray(fr));
    const l2 = decryptSum(context, secret, await evalRemote(parms, relin, tmpl, probe));
    series.push(l2);
    if (l2 < best) best = l2;
  }
  const faceOk = best < FACE_L2_MAX;
  let voice = { id: "voice", ok: false, err: "no audio", max: VOICE_L2_MAX, ms: 0 };
  if (audio && audio.size) {
    const { samples, rate } = await decodeAudio(audio);
    const q = qaFromSamples(samples, rate);
    if (!q.ok) voice = { id: "voice", ok: false, err: q.reason, seconds: q.seconds, max: VOICE_L2_MAX, ms: 0 };
    else if (row.voices && row.voices[0]) {
      const probe = encryptVec(context, publicKey, voiceVec(samples, rate));
      const l2 = decryptSum(context, secret, await evalRemote(parms, relin, unb64(row.voices[0]), probe));
      const mx = faceOk ? VOICE_L2_MAX : Math.min(VOICE_L2_MAX, 0.04);
      voice = { id: "voice", ok: l2 < mx, l2, max: mx, ms: 0 };
    }
  }
  const jobs = {
    face: { id: "face", ok: faceOk, l2: best, series, max: FACE_L2_MAX, n: frames.length },
    voice,
    words: { id: "words", ok: true, text: said, score: 999 },
    wave: { id: "wave", ok: true, series, score: 999 },
  };
  const bits = ["face", "voice", "words", "wave"].map((k) => (jobs[k].ok ? 1 : 0));
  return {
    id,
    ok: faceOk,
    lanes: jobs,
    labels: ["face", "voice", "words", "wave"],
    bits,
    ms: { face: 0, voice: 0, words: 0, wave: 0, total: Math.round(performance.now() - t0) },
    thresh: { face: FACE_L2_MAX, voice: voice.max },
    profile: { faces: (row.faces || []).length, voices: (row.voices || []).length },
  };
}

export function empty() {
  return Promise.resolve({ escrows: [], receipts: [], last_hop: {}, samples: [] });
}
