import { api, ApiError } from './api.js';
import { seal, unseal, deriveFromOath, createMaster, wrapMaster, unwrapMaster, exportMaster, importMaster, toB64, randomBytes } from './crypto.js';
import { kvGet, kvSet, kvDel, kvClear } from './keystore.js';
import { EMPTY_SUMMARY, applyEpisode } from './logic.js';
import { findExercise } from './exercises.js';

const S = {
  userId: null, name: null, key: null,
  base: null, baseRev: 0, outbox: [], summary: null,
  draftRev: 0, sync: { state: 'idle', pending: 0 }, remembered: false,
};

export const session = S;

const listeners = new Set();
export function onSync(fn) {
  listeners.add(fn);
  return () => listeners.delete(fn);
}

function setSync(state) {
  S.sync = { state, pending: S.outbox.length };
  listeners.forEach((fn) => fn(S.sync, S.summary));
}

const aad = (id) => `${S.userId}:${id}`;
const epId = (n) => `ep-${String(n).padStart(6, '0')}`;
const newEpId = () => `ep-${Date.now().toString(36)}-${toB64(randomBytes(6)).replace(/[^a-z0-9]/gi, '').toLowerCase().slice(0, 6)}`;
const clone = (x) => JSON.parse(JSON.stringify(x));

function finder(summary) {
  return (id) => findExercise(id, (summary && summary.custom) || []);
}

async function encode(id, value) {
  return seal(S.key, aad(id), value);
}

async function decode(id, doc) {
  return unseal(S.key, aad(id), doc.iv, doc.data);
}

async function cacheSet(name, docId, value) {
  await kvSet(`${name}:${S.userId}`, await encode(docId, value));
}

async function cacheGet(name, docId) {
  const sealed = await kvGet(`${name}:${S.userId}`);
  if (!sealed) return null;
  try {
    return await unseal(S.key, aad(docId), sealed.iv, sealed.data);
  } catch {
    return null;
  }
}

function reset() {
  Object.assign(S, { userId: null, name: null, key: null, base: null, baseRev: 0, outbox: [], summary: null, draftRev: 0, remembered: false });
}

async function remember(keep, extractable) {
  S.remembered = false;
  if (!keep) return kvDel('device');
  try {
    if (navigator.storage && navigator.storage.persist) navigator.storage.persist().catch(() => {});
  } catch {}
  const base = { userId: S.userId, name: S.name };
  if (await kvSet('device', { ...base, key: S.key })) {
    const back = await kvGet('device');
    if (back && back.key) return (S.remembered = true);
  }
  try {
    S.remembered = await kvSet('device', { ...base, raw: await exportMaster(await extractable()) });
  } catch {
    await kvSet('device', base);
  }
}

export async function restore() {
  const dev = await kvGet('device');
  if (dev && !dev.key && dev.raw) {
    try {
      dev.key = await importMaster(dev.raw);
    } catch {}
  }
  if (!dev || !dev.key) return { state: 'none', name: dev && dev.name };
  S.remembered = true;
  try {
    const me = await api('/api/me');
    if (me.userId !== dev.userId) {
      await kvClear();
      return { state: 'none' };
    }
    Object.assign(S, { userId: dev.userId, name: dev.name, key: dev.key });
    return { state: 'ok' };
  } catch (e) {
    if (e.status === 401) {
      await kvDel('device');
      return { state: 'none', name: dev.name };
    }
    Object.assign(S, { userId: dev.userId, name: dev.name, key: dev.key });
    return { state: 'offline' };
  }
}

export async function join(name, oath, keep, invite) {
  const salt = toB64(randomBytes(16));
  const { kek, authKey } = await deriveFromOath(oath, salt);
  const { master, wrappedKey, wrapIv } = await createMaster(kek);
  const r = await api('/api/signup', { method: 'POST', body: { name, salt, authKey, wrappedKey, wrapIv, invite } });
  reset();
  Object.assign(S, { userId: r.userId, name: r.name, key: master });
  await remember(keep, () => unwrapMaster(kek, wrappedKey, wrapIv, true));
}

export async function enter(name, oath, keep) {
  const { salt } = await api('/api/prelogin', { method: 'POST', body: { name } });
  const { kek, authKey } = await deriveFromOath(oath, salt);
  const r = await api('/api/login', { method: 'POST', body: { name, authKey } });
  const key = await unwrapMaster(kek, r.wrappedKey, r.wrapIv);
  reset();
  Object.assign(S, { userId: r.userId, name: r.name, key });
  await remember(keep, () => unwrapMaster(kek, r.wrappedKey, r.wrapIv, true));
}

export function pendingCount() {
  return S.outbox.length;
}

export async function lock() {
  try {
    await api('/api/logout', { method: 'POST', body: {} });
  } catch {}
  await kvClear();
  reset();
}

export async function changeOath(oldOath, newOath) {
  const { salt } = await api('/api/prelogin', { method: 'POST', body: { name: S.name } });
  const old = await deriveFromOath(oldOath, salt);
  const cur = await api('/api/account/key', { method: 'POST', body: { authKey: old.authKey } });
  const master = await unwrapMaster(old.kek, cur.wrappedKey, cur.wrapIv, true);
  const newSalt = toB64(randomBytes(16));
  const neu = await deriveFromOath(newOath, newSalt);
  const wrapped = await wrapMaster(neu.kek, master);
  await unwrapMaster(neu.kek, wrapped.wrappedKey, wrapped.wrapIv);
  await api('/api/account/passphrase', { method: 'POST', body: { authKey: old.authKey, salt: newSalt, newAuthKey: neu.authKey, ...wrapped } });
}

export async function destroy(oath) {
  const { salt } = await api('/api/prelogin', { method: 'POST', body: { name: S.name } });
  const { authKey } = await deriveFromOath(oath, salt);
  await api('/api/account/delete', { method: 'POST', body: { authKey } });
  await kvClear();
  reset();
}

function derive() {
  let s = clone(S.base || EMPTY_SUMMARY());
  for (const op of S.outbox) {
    if (op.kind === 'episode') s = applyEpisode(s, { ...op.ep, n: s.episodes + 1 }, finder(s));
    if (op.kind === 'custom' && !s.custom.some((c) => c.id === op.ex.id)) s.custom = [...s.custom, op.ex];
  }
  S.summary = s;
  return s;
}

async function saveOutbox() {
  await cacheSet('outbox', 'outbox', S.outbox);
}

async function fetchBase() {
  try {
    const doc = await api('/api/doc/summary');
    S.base = { ...EMPTY_SUMMARY(), ...(await decode('summary', doc)) };
    S.baseRev = doc.rev;
  } catch (e) {
    if (e.status !== 404) throw e;
    S.base = EMPTY_SUMMARY();
    S.baseRev = 0;
  }
  await cacheSet('summary', 'summary', { s: S.base, rev: S.baseRev });
}

export async function loadSummary() {
  const cached = await cacheGet('summary', 'summary');
  if (cached) {
    S.base = { ...EMPTY_SUMMARY(), ...cached.s };
    S.baseRev = cached.rev;
  }
  S.outbox = (await cacheGet('outbox', 'outbox')) || [];
  try {
    await fetchBase();
    S.offline = false;
  } catch (e) {
    if (!cached) S.base = EMPTY_SUMMARY();
    S.offline = true;
  }
  derive();
  setSync(S.outbox.length ? (S.offline ? 'offline' : 'pending') : (S.offline ? 'offline' : 'synced'));
  syncSoon(0);
  return S.summary;
}

let syncing = null;
let syncTimer = null;

export function syncSoon(ms = 400) {
  clearTimeout(syncTimer);
  syncTimer = setTimeout(() => { syncNow(); }, ms);
}

export function syncNow() {
  if (!S.key) return Promise.resolve();
  if (!syncing) syncing = runSync().finally(() => { syncing = null; });
  return syncing;
}

async function putSummary(next) {
  const r = await api('/api/doc/summary', { method: 'PUT', body: { rev: S.baseRev, ...(await encode('summary', next)) } });
  S.base = next;
  S.baseRev = r.rev;
  await cacheSet('summary', 'summary', { s: next, rev: r.rev });
}

async function pushEpisode(op) {
  for (let tries = 0; tries < 6; tries++) {
    await fetchBase();
    const ep = { ...op.ep, n: S.base.episodes + 1 };
    try {
      const r = await api('/api/doc/' + op.id, { method: 'PUT', body: { rev: op.rev || 0, ...(await encode(op.id, ep)) } });
      op.rev = r.rev;
    } catch (e) {
      if (e.status !== 409) throw e;
      op.rev = e.data && e.data.current ? e.data.current.rev : 0;
      continue;
    }
    try {
      await putSummary(applyEpisode(S.base, ep, finder(S.base)));
      await cacheSet('ep:' + op.id, op.id, ep);
      return;
    } catch (e) {
      if (e.status !== 409) throw e;
    }
  }
  throw new ApiError(409, 'Kept changing elsewhere. Will retry.');
}

async function pushCustom(op) {
  for (let tries = 0; tries < 6; tries++) {
    await fetchBase();
    if (S.base.custom.some((c) => c.id === op.ex.id)) return;
    try {
      await putSummary({ ...S.base, custom: [...S.base.custom, op.ex] });
      return;
    } catch (e) {
      if (e.status !== 409) throw e;
    }
  }
  throw new ApiError(409, 'Kept changing elsewhere. Will retry.');
}

async function flushDraftDelete() {
  if (!(await kvGet('draftdel:' + S.userId))) return;
  await api('/api/doc/draft', { method: 'DELETE' });
  await kvDel('draftdel:' + S.userId);
}

async function runSync() {
  try {
    await flushDraftDelete();
  } catch {}
  if (!S.outbox.length) {
    try {
      const before = S.baseRev;
      await fetchBase();
      S.offline = false;
      derive();
      setSync('synced');
      return before !== S.baseRev;
    } catch {
      S.offline = true;
      setSync('offline');
      return false;
    }
  }
  setSync('syncing');
  try {
    while (S.outbox.length) {
      const op = S.outbox[0];
      if (op.kind === 'episode') await pushEpisode(op);
      if (op.kind === 'custom') await pushCustom(op);
      S.outbox.shift();
      await saveOutbox();
    }
    S.offline = false;
    derive();
    setSync('synced');
    return true;
  } catch (e) {
    S.offline = e.status === 0;
    await saveOutbox();
    derive();
    setSync(e.status === 0 ? 'offline' : 'error');
    return false;
  }
}

export async function saveEpisode(build) {
  const id = newEpId();
  const ep = { ...build(S.summary.episodes + 1), id };
  S.outbox.push({ kind: 'episode', id, ep, rev: 0 });
  await saveOutbox();
  await cacheSet('ep:' + id, id, ep);
  derive();
  setSync('pending');
  syncSoon(0);
  return ep;
}

export async function addCustom(ex) {
  S.outbox.push({ kind: 'custom', ex });
  await saveOutbox();
  derive();
  setSync('pending');
  syncSoon(0);
  return S.summary;
}

export async function getEpisode(n) {
  const entry = S.summary.recent.find((r) => r.n === n);
  const id = (entry && entry.id) || epId(n);
  const pending = S.outbox.find((op) => op.kind === 'episode' && op.id === id);
  if (pending) return { ...pending.ep, n };
  const cached = await cacheGet('ep:' + id, id);
  if (cached) return { ...cached, n };
  const doc = await api('/api/doc/' + id);
  const ep = await decode(id, doc);
  await cacheSet('ep:' + id, id, ep);
  return { ...ep, n };
}

export async function loadDraft() {
  const local = await cacheGet('draft', 'draft');
  if (!local && (await kvGet('draftdel:' + S.userId))) return null;
  try {
    const doc = await api('/api/doc/draft');
    S.draftRev = doc.rev;
    const remote = await decode('draft', doc);
    if (local && (local.savedAt || 0) > (remote.savedAt || 0)) return local;
    return remote;
  } catch (e) {
    if (e.status === 404) S.draftRev = 0;
    return local;
  }
}

let draftTimer = null;
let draftPending = null;

export function saveDraft(draft, onStatus) {
  draft.savedAt = Date.now();
  draftPending = draft;
  cacheSet('draft', 'draft', draft);
  clearTimeout(draftTimer);
  onStatus('saving');
  draftTimer = setTimeout(() => flushDraft(onStatus), 1200);
}

async function flushDraft(onStatus) {
  const draft = draftPending;
  if (!draft) return;
  for (let i = 0; i < 3; i++) {
    try {
      const r = await api('/api/doc/draft', { method: 'PUT', body: { rev: S.draftRev, ...(await encode('draft', draft)) } });
      S.draftRev = r.rev;
      if (draftPending === draft) draftPending = null;
      onStatus('saved');
      return;
    } catch (e) {
      if (e.status === 409) {
        S.draftRev = e.data && e.data.current ? e.data.current.rev : 0;
        continue;
      }
      onStatus('local');
      return;
    }
  }
  onStatus('local');
}

export function retryDraft(onStatus) {
  if (draftPending) flushDraft(onStatus);
}

export async function clearDraft() {
  clearTimeout(draftTimer);
  draftPending = null;
  await kvDel('draft:' + S.userId);
  try {
    await api('/api/doc/draft', { method: 'DELETE' });
  } catch {
    await kvSet('draftdel:' + S.userId, true);
  }
  S.draftRev = 0;
}

export async function exportAll() {
  const { docs } = await api('/api/docs');
  const out = { app: 'Training Arc', name: S.name, exportedAt: new Date().toISOString(), docs: {} };
  for (const d of docs) {
    try {
      out.docs[d.id] = await decode(d.id, d);
    } catch {
      out.docs[d.id] = { error: 'Could not decrypt' };
    }
  }
  if (S.outbox.length) out.notSyncedYet = S.outbox.map((op) => (op.kind === 'episode' ? op.ep : op.ex));
  return out;
}
