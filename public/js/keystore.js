const DB = 'training-arc';
const STORE = 'kv';

function db() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB, 1);
    req.onupgradeneeded = () => req.result.createObjectStore(STORE);
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function tx(mode, fn) {
  const d = await db();
  return new Promise((resolve, reject) => {
    const t = d.transaction(STORE, mode);
    const req = fn(t.objectStore(STORE));
    t.oncomplete = () => resolve(req && req.result);
    t.onerror = () => reject(t.error);
  });
}

export async function kvGet(k) {
  try {
    return await tx('readonly', (s) => s.get(k));
  } catch {
    return undefined;
  }
}

export async function kvSet(k, v) {
  try {
    await tx('readwrite', (s) => s.put(v, k));
    return true;
  } catch {
    return false;
  }
}

export async function kvDel(k) {
  try {
    await tx('readwrite', (s) => s.delete(k));
  } catch {}
}

export async function kvClear() {
  try {
    await tx('readwrite', (s) => s.clear());
  } catch {}
}
