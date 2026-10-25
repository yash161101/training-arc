import { api, ApiError } from './api.js';
import { seal, unseal, deriveFromOath, createMaster, unwrapMaster, toB64, randomBytes } from './crypto.js';
import { kvGet, kvSet, kvDel, kvClear } from './keystore.js';
import { EMPTY_SUMMARY, applyEpisode } from './logic.js';

const S = { userId: null, name: null, key: null, summary: null, summaryRev: 0, draftRev: 0 };

export const session = S;

const aad = (id) => `${S.userId}:${id}`;
const epId = (n) => `ep-${String(n).padStart(6, '0')}`;

async function encode(id, value) {
  return seal(S.key, aad(id), value);
}

async function decode(id, doc) {
  return unseal(S.key, aad(id), doc.iv, doc.data);
}

async function remember(keep) {
  if (keep) await kvSet('device', { userId: S.userId, name: S.name, key: S.key });
  else await kvDel('device');
}

export async function restore() {
  const dev = await kvGet('device');
  if (!dev || !dev.key) return { state: 'none', name: dev && dev.name };
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
  Object.assign(S, { userId: r.userId, name: r.name, key: master, summary: null, summaryRev: 0, draftRev: 0 });
  await remember(keep);
}

export async function enter(name, oath, keep) {
  const { salt } = await api('/api/prelogin', { method: 'POST', body: { name } });
  const { kek, authKey } = await deriveFromOath(oath, salt);
  const r = await api('/api/login', { method: 'POST', body: { name, authKey } });
  const key = await unwrapMaster(kek, r.wrappedKey, r.wrapIv);
  Object.assign(S, { userId: r.userId, name: r.name, key, summary: null, summaryRev: 0, draftRev: 0 });
  await remember(keep);
}

export async function lock() {
  try {
    await api('/api/logout', { method: 'POST', body: {} });
  } catch {}
  await kvClear();
  Object.assign(S, { userId: null, name: null, key: null, summary: null, summaryRev: 0, draftRev: 0 });
}

export async function destroy(oath) {
  const { salt } = await api('/api/prelogin', { method: 'POST', body: { name: S.name } });
  const { authKey } = await deriveFromOath(oath, salt);
  await api('/api/account/delete', { method: 'POST', body: { authKey } });
  await kvClear();
  Object.assign(S, { userId: null, name: null, key: null, summary: null });
}

export async function loadSummary() {
  try {
    const doc = await api('/api/doc/summary');
    S.summary = { ...EMPTY_SUMMARY(), ...(await decode('summary', doc)) };
    S.summaryRev = doc.rev;
    await kvSet('summary:' + S.userId, await encode('summary', { s: S.summary, rev: S.summaryRev }));
  } catch (e) {
    if (e.status === 404) {
      S.summary = EMPTY_SUMMARY();
      S.summaryRev = 0;
    } else {
      const cached = await kvGet('summary:' + S.userId);
      if (!cached) throw e;
      const c = await unseal(S.key, aad('summary'), cached.iv, cached.data);
      S.summary = c.s;
      S.summaryRev = c.rev;
      S.offline = true;
    }
  }
  return S.summary;
}

async function updateSummary(mutate) {
  for (let i = 0; i < 4; i++) {
    const next = mutate(S.summary);
    const body = { rev: S.summaryRev, ...(await encode('summary', next)) };
    try {
      const r = await api('/api/doc/summary', { method: 'PUT', body });
      S.summary = next;
      S.summaryRev = r.rev;
      await kvSet('summary:' + S.userId, await encode('summary', { s: next, rev: r.rev }));
      return next;
    } catch (e) {
      if (e.status !== 409) throw e;
      const cur = e.data && e.data.current;
      if (cur) {
        S.summary = { ...EMPTY_SUMMARY(), ...(await decode('summary', cur)) };
        S.summaryRev = cur.rev;
      } else {
        S.summary = EMPTY_SUMMARY();
        S.summaryRev = 0;
      }
    }
  }
  throw new ApiError(409, 'Could not save. Try again.');
}

export async function saveEpisode(build, find) {
  for (let i = 0; i < 4; i++) {
    const n = S.summary.episodes + 1;
    const ep = build(n);
    try {
      await api('/api/doc/' + epId(n), { method: 'PUT', body: { rev: 0, ...(await encode(epId(n), ep)) } });
    } catch (e) {
      if (e.status !== 409) throw e;
      await loadSummary();
      S.summary.episodes = Math.max(S.summary.episodes, n);
      continue;
    }
    await updateSummary((s) => applyEpisode(s, ep, find));
    return ep;
  }
  throw new ApiError(409, 'Could not save. Try again.');
}

export async function addCustom(ex) {
  return updateSummary((s) => ({ ...s, custom: [...(s.custom || []), ex] }));
}

export async function getEpisode(n) {
  const doc = await api('/api/doc/' + epId(n));
  return decode(epId(n), doc);
}

export async function loadDraft() {
  try {
    const doc = await api('/api/doc/draft');
    S.draftRev = doc.rev;
    return await decode('draft', doc);
  } catch (e) {
    if (e.status === 404) {
      S.draftRev = 0;
      const local = await kvGet('draft:' + S.userId);
      return local ? unseal(S.key, aad('draft'), local.iv, local.data) : null;
    }
    const local = await kvGet('draft:' + S.userId);
    return local ? unseal(S.key, aad('draft'), local.iv, local.data) : null;
  }
}

let draftTimer = null;
let draftPending = null;

export function saveDraft(draft, onStatus) {
  draftPending = draft;
  encode('draft', draft).then((sealed) => kvSet('draft:' + S.userId, sealed));
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

export async function clearDraft() {
  clearTimeout(draftTimer);
  draftPending = null;
  await kvDel('draft:' + S.userId);
  try {
    await api('/api/doc/draft', { method: 'DELETE' });
  } catch {}
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
  return out;
}
