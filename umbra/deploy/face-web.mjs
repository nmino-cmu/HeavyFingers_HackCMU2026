#!/usr/bin/env node
import http from "node:http";
import SEAL from "node-seal";

const PORT = Number(process.env.UMBRA_FACE_WEB_PORT || 8090);
const BIND = process.env.UMBRA_FACE_WEB_BIND || "10.20.0.6";
const POLY = 8192;

function unpackN(body, n) {
  const view = new DataView(body.buffer, body.byteOffset, body.byteLength);
  const parts = [];
  let o = 0;
  for (let i = 0; i < n; i++) {
    const len = view.getUint32(o);
    o += 4;
    parts.push(body.subarray(o, o + len));
    o += len;
  }
  return parts;
}

const seal = await SEAL();
const ZSTD = seal.ComprModeType.zstd;

function evalL2(body) {
  const [parmBytes, relinBytes, tmpl, probe] = unpackN(body, 4);
  const p2 = new seal.EncryptionParameters(seal.SchemeType.ckks);
  p2.loadFromArray(parmBytes, ZSTD);
  if (p2.polyModulusDegree() !== POLY) throw new Error("bad degree");
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

function cors(req, res) {
  const origin = req.headers.origin || "";
  if (/^https:\/\/(www\.)?nickmino\.com$/.test(origin) || /sslip\.io$/.test(origin)) {
    res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Vary", "Origin");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  }
}

const server = http.createServer((req, res) => {
  cors(req, res);
  if (req.method === "OPTIONS") {
    res.writeHead(204);
    res.end();
    return;
  }
  const path = (req.url || "/").split("?")[0];
  if (req.method === "GET" && (path === "/health" || path === "/face-web/health")) {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ role: "face-web", stack: "node-seal-ckks" }));
    return;
  }
  if (req.method !== "POST") {
    res.writeHead(404);
    res.end("no");
    return;
  }
  const chunks = [];
  req.on("data", (c) => chunks.push(c));
  req.on("end", () => {
    try {
      const body = Buffer.concat(chunks);
      const out = evalL2(new Uint8Array(body));
      res.writeHead(200, { "Content-Type": "application/octet-stream" });
      res.end(Buffer.from(out));
    } catch (e) {
      res.writeHead(400, { "Content-Type": "text/plain" });
      res.end(String(e && e.message ? e.message : e).slice(0, 200));
    }
  });
});

server.listen(PORT, BIND, () => {
  console.log("face-web", BIND + ":" + PORT);
});
