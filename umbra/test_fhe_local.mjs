import SEAL from "./web/vendor/node-seal/index_throws.js";

const N = 8192;
const SCALE = 2 ** 40;
const PIXELS = 4096;

function vec(seed) {
  const out = new Float64Array(PIXELS);
  for (let i = 0; i < PIXELS; i++) out[i] = ((i * 17 + seed * 31) % 251) / 255;
  return out;
}

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
const parms = new seal.EncryptionParameters(seal.SchemeType.ckks);
parms.setPolyModulusDegree(N);
parms.setCoeffModulus(seal.CoeffModulus.Create(N, Int32Array.from([60, 40, 40, 60])));
const context = new seal.SEALContext(parms, true, seal.SecLevelType.tc128);
const keygen = new seal.KeyGenerator(context);
const secret = keygen.secretKey();
const publicKey = keygen.createPublicKey();
const relinSer = keygen.createRelinKeysSerializable();
const encoder = new seal.CKKSEncoder(context);
const encryptor = new seal.Encryptor(context, publicKey);
const decryptor = new seal.Decryptor(context, secret);

function encrypt(arr) {
  const plain = new seal.Plaintext();
  encoder.encode(arr, SCALE, plain);
  const ct = new seal.Ciphertext();
  encryptor.encrypt(plain, ct);
  return ct.saveToArray(ZSTD);
}

function evalL2(body) {
  const [parmBytes, relinBytes, tmpl, probe] = unpackN(body, 4);
  const p2 = new seal.EncryptionParameters(seal.SchemeType.ckks);
  p2.loadFromArray(parmBytes, ZSTD);
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

function decryptSum(ctBytes) {
  const ct = new seal.Ciphertext();
  ct.loadFromArray(context, ctBytes, ZSTD);
  const plain = new seal.Plaintext();
  decryptor.decrypt(ct, plain);
  const vals = encoder.decodeFloat64(plain);
  let s = 0;
  for (let i = 0; i < PIXELS; i++) s += vals[i];
  return s;
}

const a = vec(1);
const same = decryptSum(evalL2(concatPack([parms.saveToArray(ZSTD), relinSer.saveToArray(ZSTD), encrypt(a), encrypt(a)])));
const other = decryptSum(evalL2(concatPack([parms.saveToArray(ZSTD), relinSer.saveToArray(ZSTD), encrypt(a), encrypt(vec(9))])));
if (!(same < 1 && other > 10)) throw new Error("sep " + same + " " + other);
console.log("SEAL_L2 ok", same, other);
