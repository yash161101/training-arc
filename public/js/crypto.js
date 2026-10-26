const te = new TextEncoder();
const td = new TextDecoder();

export const ITERATIONS = 600000;

export function toB64(buf) {
  const b = new Uint8Array(buf);
  let s = '';
  for (let i = 0; i < b.length; i += 0x8000) s += String.fromCharCode.apply(null, b.subarray(i, i + 0x8000));
  return btoa(s);
}

export function fromB64(s) {
  return Uint8Array.from(atob(s), (c) => c.charCodeAt(0));
}

export function randomBytes(n) {
  return crypto.getRandomValues(new Uint8Array(n));
}

export function normalizeOath(oath) {
  return oath.normalize('NFKC').toLowerCase().replace(/\s+/g, ' ').trim();
}

export function oathProblem(oath) {
  const o = normalizeOath(oath);
  if (o.length < 10) return 'Use at least 10 characters.';
  if (new Set(o.replace(/ /g, '')).size < 4) return 'Too simple. Mix it up a bit.';
  return '';
}

export async function deriveFromOath(oath, saltB64) {
  const base = await crypto.subtle.importKey('raw', te.encode(normalizeOath(oath)), 'PBKDF2', false, ['deriveBits']);
  const bits = new Uint8Array(await crypto.subtle.deriveBits(
    { name: 'PBKDF2', hash: 'SHA-256', salt: fromB64(saltB64), iterations: ITERATIONS }, base, 512
  ));
  const kek = await crypto.subtle.importKey('raw', bits.slice(0, 32), 'AES-GCM', false, ['wrapKey', 'unwrapKey']);
  return { kek, authKey: toB64(bits.slice(32)) };
}

export function unwrapMaster(kek, wrappedKey, wrapIv, extractable = false) {
  return crypto.subtle.unwrapKey(
    'raw', fromB64(wrappedKey), kek, { name: 'AES-GCM', iv: fromB64(wrapIv) },
    { name: 'AES-GCM', length: 256 }, extractable, ['encrypt', 'decrypt']
  );
}

export async function exportMaster(key) {
  return toB64(await crypto.subtle.exportKey('raw', key));
}

export function importMaster(raw) {
  return crypto.subtle.importKey('raw', fromB64(raw), { name: 'AES-GCM', length: 256 }, false, ['encrypt', 'decrypt']);
}

export async function createMaster(kek) {
  const key = await crypto.subtle.generateKey({ name: 'AES-GCM', length: 256 }, true, ['encrypt', 'decrypt']);
  const iv = randomBytes(12);
  const wrapped = await crypto.subtle.wrapKey('raw', key, kek, { name: 'AES-GCM', iv });
  const wrappedKey = toB64(wrapped);
  const wrapIv = toB64(iv);
  return { master: await unwrapMaster(kek, wrappedKey, wrapIv), wrappedKey, wrapIv };
}

export async function seal(key, aad, value) {
  const iv = randomBytes(12);
  const data = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv, additionalData: te.encode(aad) }, key, te.encode(JSON.stringify(value))
  );
  return { iv: toB64(iv), data: toB64(data) };
}

export async function unseal(key, aad, iv, data) {
  const plain = await crypto.subtle.decrypt(
    { name: 'AES-GCM', iv: fromB64(iv), additionalData: te.encode(aad) }, key, fromB64(data)
  );
  return JSON.parse(td.decode(plain));
}
