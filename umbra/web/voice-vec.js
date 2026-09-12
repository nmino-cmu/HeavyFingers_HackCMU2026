/* 16-D log-band voice template. Same fn on enroll and probe. */
const PIXELS = 4096;
const VOICE_N = 16;

function nextPow2(n) {
  let p = 1;
  while (p < n) p <<= 1;
  return p;
}

function fft(re, im) {
  const n = re.length;
  for (let i = 1, j = 0; i < n; i++) {
    let bit = n >> 1;
    for (; j & bit; bit >>= 1) j ^= bit;
    j ^= bit;
    if (i < j) {
      const tr = re[i];
      re[i] = re[j];
      re[j] = tr;
      const ti = im[i];
      im[i] = im[j];
      im[j] = ti;
    }
  }
  for (let len = 2; len <= n; len <<= 1) {
    const ang = (-2 * Math.PI) / len;
    const wlenRe = Math.cos(ang);
    const wlenIm = Math.sin(ang);
    for (let i = 0; i < n; i += len) {
      let wRe = 1;
      let wIm = 0;
      const half = len >> 1;
      for (let j = 0; j < half; j++) {
        const i2 = i + j + half;
        const vr = re[i2] * wRe - im[i2] * wIm;
        const vi = re[i2] * wIm + im[i2] * wRe;
        re[i2] = re[i + j] - vr;
        im[i2] = im[i + j] - vi;
        re[i + j] += vr;
        im[i + j] += vi;
        const nRe = wRe * wlenRe - wIm * wlenIm;
        wIm = wRe * wlenIm + wIm * wlenRe;
        wRe = nRe;
      }
    }
  }
}

function band(slice, rate) {
  const n0 = slice.length;
  const n = nextPow2(n0);
  const re = new Float64Array(n);
  const im = new Float64Array(n);
  for (let i = 0; i < n0; i++) {
    const w = 0.5 * (1 - Math.cos((2 * Math.PI * i) / (n0 - 1)));
    re[i] = slice[i] * w;
  }
  fft(re, im);
  const spec = new Float64Array((n >> 1) + 1);
  for (let k = 0; k < spec.length; k++) spec[k] = re[k] * re[k] + im[k] * im[k];
  const hi = Math.min(7000, rate / 2 - 1);
  const edges = [];
  for (let i = 0; i <= VOICE_N; i++) edges.push(80 * Math.pow(hi / 80, i / VOICE_N));
  const vec = [];
  for (let i = 0; i < VOICE_N; i++) {
    let acc = 0;
    let c = 0;
    for (let k = 0; k < spec.length; k++) {
      const f = (k * rate) / n;
      if (f >= edges[i] && f < edges[i + 1]) {
        acc += spec[k];
        c++;
      }
    }
    vec.push(Math.log10((c ? acc / c : 0) + 1e-12));
  }
  return vec;
}

export function voiceVec(samples, rate) {
  let x = samples;
  const env = new Float32Array(x.length);
  let mx = 0;
  for (let i = 0; i < x.length; i++) {
    env[i] = Math.abs(x[i]);
    if (env[i] > mx) mx = env[i];
  }
  const thr = Math.max(0.01, 0.12 * mx);
  let a = 0;
  let b = x.length - 1;
  while (a < b && env[a] <= thr) a++;
  while (b > a && env[b] <= thr) b--;
  x = x.subarray(a, b + 1);
  const win = Math.max(512, Math.floor(rate * 1.0));
  const hop = Math.max(256, Math.floor(rate * 0.5));
  let v;
  if (x.length < win) {
    const pad = new Float32Array(Math.max(512, x.length));
    pad.set(x);
    v = band(pad, rate);
  } else {
    const acc = new Array(VOICE_N).fill(0);
    let nwin = 0;
    for (let i = 0; i + win <= x.length; i += hop) {
      const w = band(x.subarray(i, i + win), rate);
      for (let j = 0; j < VOICE_N; j++) acc[j] += w[j];
      nwin++;
    }
    v = acc.map((t) => t / nwin);
  }
  const mean = v.reduce((p, q) => p + q, 0) / VOICE_N;
  v = v.map((t) => t - mean);
  const nrm = Math.hypot(...v) || 1;
  const out = new Float64Array(PIXELS);
  for (let i = 0; i < VOICE_N; i++) out[i] = v[i] / nrm;
  return out;
}
