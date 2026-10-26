const DAY = 86400000;
const SESSION_DAYS = 180;
const MAX_DOC = 768 * 1024;
const NAME_RE = /^[a-z0-9_]{3,20}$/;
const B64_RE = /^[A-Za-z0-9+/]+={0,2}$/;
const DOC_RE = /^[a-z0-9-]{1,40}$/;
const PREFIX_RE = /^[a-z0-9-]{0,40}$/;

const enc = new TextEncoder();

class HttpError extends Error {
  constructor(status, message, extra) {
    super(message);
    this.status = status;
    this.extra = extra;
  }
}

const SECURITY = {
  'x-content-type-options': 'nosniff',
  'referrer-policy': 'no-referrer',
  'x-frame-options': 'DENY',
  'cache-control': 'no-store',
};

function json(data, status = 200, headers = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', ...SECURITY, ...headers },
  });
}

function b64(bytes) {
  let s = '';
  for (const b of new Uint8Array(bytes)) s += String.fromCharCode(b);
  return btoa(s);
}

function token() {
  return b64(crypto.getRandomValues(new Uint8Array(32))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

async function sha(text) {
  return b64(await crypto.subtle.digest('SHA-256', enc.encode(text)));
}

function same(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string' || a.length !== b.length) return false;
  let r = 0;
  for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return r === 0;
}

function sessionCookie(value, maxAge) {
  return `__Host-ta=${value}; Path=/; Secure; HttpOnly; SameSite=Strict; Max-Age=${maxAge}`;
}

function b64Field(v, min, max) {
  if (typeof v !== 'string' || v.length < min || v.length > max || !B64_RE.test(v)) throw new HttpError(400, 'Bad request');
  return v;
}

async function readJson(req) {
  if (!(req.headers.get('content-type') || '').startsWith('application/json')) throw new HttpError(415, 'Send JSON');
  const text = await req.text();
  if (text.length > MAX_DOC * 1.4) throw new HttpError(413, 'Too large');
  try {
    return JSON.parse(text);
  } catch {
    throw new HttpError(400, 'Bad request');
  }
}

async function pepper(env) {
  const get = () => env.DB.prepare('SELECT v FROM meta WHERE k = ?').bind('pepper').first();
  let row = await get();
  if (!row) {
    await env.DB.prepare('INSERT OR IGNORE INTO meta (k, v) VALUES (?, ?)').bind('pepper', token()).run();
    row = await get();
  }
  return row.v;
}

async function limit(env, key, max, windowMs) {
  const now = Date.now();
  const row = await env.DB.prepare('SELECT n, reset_at FROM limits WHERE k = ?').bind(key).first();
  if (!row || row.reset_at < now) {
    await env.DB.prepare('INSERT INTO limits (k, n, reset_at) VALUES (?, 1, ?) ON CONFLICT(k) DO UPDATE SET n = 1, reset_at = excluded.reset_at')
      .bind(key, now + windowMs).run();
    return;
  }
  if (row.n >= max) throw new HttpError(429, 'Too many tries. Wait a few minutes.');
  await env.DB.prepare('UPDATE limits SET n = n + 1 WHERE k = ?').bind(key).run();
}

async function startSession(env, userId) {
  const t = token();
  await env.DB.prepare('INSERT INTO sessions (token_hash, user_id, expires_at) VALUES (?, ?, ?)')
    .bind(await sha(t), userId, Date.now() + SESSION_DAYS * DAY).run();
  if (Math.random() < 0.05) await env.DB.prepare('DELETE FROM sessions WHERE expires_at < ?').bind(Date.now()).run();
  return sessionCookie(t, SESSION_DAYS * 86400);
}

async function session(req, env) {
  const m = /(?:^|;\s*)__Host-ta=([A-Za-z0-9_-]{20,})/.exec(req.headers.get('cookie') || '');
  if (!m) throw new HttpError(401, 'Signed out');
  const tokenHash = await sha(m[1]);
  const row = await env.DB.prepare('SELECT user_id, expires_at FROM sessions WHERE token_hash = ?').bind(tokenHash).first();
  if (!row || row.expires_at < Date.now()) throw new HttpError(401, 'Signed out');
  return { userId: row.user_id, tokenHash, token: m[1], expiresAt: row.expires_at };
}

function cleanName(v) {
  const name = typeof v === 'string' ? v.trim().toLowerCase() : '';
  if (!NAME_RE.test(name)) throw new HttpError(400, 'Names are 3 to 20 letters, numbers or _');
  return name;
}

function docRow(r) {
  return { id: r.id, rev: r.rev, iv: r.iv, data: r.data };
}

async function signup(req, env, ip) {
  await limit(env, 'signup:' + ip, 5, 60 * 60 * 1000);
  const b = await readJson(req);
  if (!env.INVITE_CODE) throw new HttpError(403, 'Sign ups are closed');
  const invite = typeof b.invite === 'string' ? b.invite.trim().toLowerCase() : '';
  if (!same(await sha(invite), await sha(env.INVITE_CODE.trim().toLowerCase()))) throw new HttpError(403, 'That invite code isn\u2019t right');
  const name = cleanName(b.name);
  const salt = b64Field(b.salt, 16, 64);
  const authKey = b64Field(b.authKey, 40, 64);
  const wrappedKey = b64Field(b.wrappedKey, 40, 128);
  const wrapIv = b64Field(b.wrapIv, 16, 24);
  const id = crypto.randomUUID();
  const res = await env.DB.prepare(
    'INSERT OR IGNORE INTO users (id, name, salt, auth_hash, wrapped_key, wrap_iv, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)'
  ).bind(id, name, salt, await sha(authKey), wrappedKey, wrapIv, Date.now()).run();
  if (!res.meta.changes) throw new HttpError(409, 'That name is taken');
  return json({ userId: id, name }, 200, { 'set-cookie': await startSession(env, id) });
}

async function prelogin(req, env, ip) {
  await limit(env, 'pre:' + ip, 40, 10 * 60 * 1000);
  const name = cleanName((await readJson(req)).name);
  const row = await env.DB.prepare('SELECT salt FROM users WHERE name = ?').bind(name).first();
  if (row) return json({ salt: row.salt });
  const fake = await sha((await pepper(env)) + ':' + name);
  return json({ salt: fake.slice(0, 24) });
}

async function checkAuth(env, user, authKey, wrong) {
  const now = Date.now();
  if (user.locked_until > now) {
    const mins = Math.ceil((user.locked_until - now) / 60000);
    throw new HttpError(429, `Too many wrong tries. Try again in ${mins} min.`);
  }
  if (!same(await sha(authKey), user.auth_hash)) {
    const fails = user.fails + 1;
    await env.DB.prepare('UPDATE users SET fails = ?, locked_until = ? WHERE id = ?')
      .bind(fails >= 5 ? 0 : fails, fails >= 5 ? now + 15 * 60000 : 0, user.id).run();
    throw new HttpError(401, wrong);
  }
  if (user.fails) await env.DB.prepare('UPDATE users SET fails = 0 WHERE id = ?').bind(user.id).run();
}

async function accountKey(req, env, ip) {
  await limit(env, 'rekey:' + ip, 20, 10 * 60 * 1000);
  const s = await session(req, env);
  const authKey = b64Field((await readJson(req)).authKey, 40, 64);
  const user = await env.DB.prepare('SELECT * FROM users WHERE id = ?').bind(s.userId).first();
  if (!user) throw new HttpError(401, 'Signed out');
  await checkAuth(env, user, authKey, 'That isn\u2019t your current passphrase');
  return json({ wrappedKey: user.wrapped_key, wrapIv: user.wrap_iv });
}

async function changePassphrase(req, env, ip) {
  await limit(env, 'rekey:' + ip, 20, 10 * 60 * 1000);
  const s = await session(req, env);
  const b = await readJson(req);
  const authKey = b64Field(b.authKey, 40, 64);
  const salt = b64Field(b.salt, 16, 64);
  const newAuthKey = b64Field(b.newAuthKey, 40, 64);
  const wrappedKey = b64Field(b.wrappedKey, 40, 128);
  const wrapIv = b64Field(b.wrapIv, 16, 24);
  const user = await env.DB.prepare('SELECT * FROM users WHERE id = ?').bind(s.userId).first();
  if (!user) throw new HttpError(401, 'Signed out');
  await checkAuth(env, user, authKey, 'That isn\u2019t your current passphrase');
  const res = await env.DB.prepare('UPDATE users SET salt = ?, auth_hash = ?, wrapped_key = ?, wrap_iv = ? WHERE id = ? AND auth_hash = ?')
    .bind(salt, await sha(newAuthKey), wrappedKey, wrapIv, user.id, user.auth_hash).run();
  if (!res.meta.changes) throw new HttpError(409, 'Your passphrase just changed somewhere else. Try again.');
  return json({ ok: true });
}

async function login(req, env, ip) {
  await limit(env, 'login:' + ip, 30, 10 * 60 * 1000);
  const b = await readJson(req);
  const name = cleanName(b.name);
  const authKey = b64Field(b.authKey, 40, 64);
  const user = await env.DB.prepare('SELECT * FROM users WHERE name = ?').bind(name).first();
  if (!user) {
    await sha(authKey);
    throw new HttpError(401, 'Wrong name or passphrase');
  }
  await checkAuth(env, user, authKey, 'Wrong name or passphrase');
  return json(
    { userId: user.id, name: user.name, wrappedKey: user.wrapped_key, wrapIv: user.wrap_iv },
    200,
    { 'set-cookie': await startSession(env, user.id) }
  );
}

async function me(req, env) {
  const s = await session(req, env);
  const user = await env.DB.prepare('SELECT id, name FROM users WHERE id = ?').bind(s.userId).first();
  if (!user) throw new HttpError(401, 'Signed out');
  const now = Date.now();
  if (s.expiresAt - now < (SESSION_DAYS - 1) * DAY) {
    await env.DB.prepare('UPDATE sessions SET expires_at = ? WHERE token_hash = ?').bind(now + SESSION_DAYS * DAY, s.tokenHash).run();
    return json({ userId: user.id, name: user.name }, 200, { 'set-cookie': sessionCookie(s.token, SESSION_DAYS * 86400) });
  }
  return json({ userId: user.id, name: user.name });
}

async function sky(req, env) {
  await session(req, env);
  const cf = req.cf || {};
  const lat = Number(cf.latitude);
  const lon = Number(cf.longitude);
  const has = Number.isFinite(lat) && Number.isFinite(lon) && (lat !== 0 || lon !== 0);
  const out = {
    city: typeof cf.city === 'string' ? cf.city : null,
    country: typeof cf.country === 'string' ? cf.country : null,
    lat: has ? Math.round(lat * 10) / 10 : null,
    lon: has ? Math.round(lon * 10) / 10 : null,
    weather: null,
  };
  if (has) {
    const la = Math.round(lat * 2) / 2;
    const lo = Math.round(lon * 2) / 2;
    const key = new Request(`https://sky.cache/v1/${la},${lo}`);
    let hit = null;
    try {
      hit = await caches.default.match(key);
    } catch {}
    if (!hit) {
      try {
        const r = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${la}&longitude=${lo}&current=weather_code,cloud_cover,precipitation`, { signal: AbortSignal.timeout(4000) });
        if (r.ok) {
          const j = await r.json();
          const c = j.current || {};
          hit = new Response(JSON.stringify({ code: c.weather_code, cloud: c.cloud_cover, rain: c.precipitation }), { headers: { 'content-type': 'application/json', 'cache-control': 'max-age=1800' } });
          try {
            await caches.default.put(key, hit.clone());
          } catch {}
        }
      } catch {}
    }
    if (hit) {
      try {
        out.weather = await hit.json();
      } catch {}
    }
  }
  return json(out);
}

async function logout(req, env) {
  try {
    const s = await session(req, env);
    await env.DB.prepare('DELETE FROM sessions WHERE token_hash = ?').bind(s.tokenHash).run();
  } catch {}
  return json({ ok: true }, 200, { 'set-cookie': sessionCookie('', 0) });
}

async function deleteAccount(req, env) {
  const s = await session(req, env);
  const authKey = b64Field((await readJson(req)).authKey, 40, 64);
  const user = await env.DB.prepare('SELECT auth_hash FROM users WHERE id = ?').bind(s.userId).first();
  if (!user || !same(await sha(authKey), user.auth_hash)) throw new HttpError(401, 'Wrong passphrase');
  await env.DB.batch([
    env.DB.prepare('DELETE FROM docs WHERE user_id = ?').bind(s.userId),
    env.DB.prepare('DELETE FROM sessions WHERE user_id = ?').bind(s.userId),
    env.DB.prepare('DELETE FROM users WHERE id = ?').bind(s.userId),
  ]);
  return json({ ok: true }, 200, { 'set-cookie': sessionCookie('', 0) });
}

async function listDocs(req, env, url) {
  const s = await session(req, env);
  const prefix = url.searchParams.get('prefix') || '';
  if (!PREFIX_RE.test(prefix)) throw new HttpError(400, 'Bad request');
  const { results } = await env.DB.prepare('SELECT id, rev, iv, data FROM docs WHERE user_id = ? AND id LIKE ? ORDER BY id LIMIT 2000')
    .bind(s.userId, prefix + '%').all();
  return json({ docs: results.map(docRow) });
}

async function getDoc(req, env, id) {
  const s = await session(req, env);
  const row = await env.DB.prepare('SELECT id, rev, iv, data FROM docs WHERE user_id = ? AND id = ?').bind(s.userId, id).first();
  if (!row) throw new HttpError(404, 'Not found');
  return json(docRow(row));
}

async function putDoc(req, env, id) {
  const s = await session(req, env);
  const b = await readJson(req);
  const rev = Number.isInteger(b.rev) && b.rev >= 0 ? b.rev : -1;
  if (rev < 0) throw new HttpError(400, 'Bad request');
  const iv = b64Field(b.iv, 16, 24);
  const data = b64Field(b.data, 4, MAX_DOC);
  const now = Date.now();
  const res = rev === 0
    ? await env.DB.prepare('INSERT OR IGNORE INTO docs (user_id, id, rev, iv, data, updated_at) VALUES (?, ?, 1, ?, ?, ?)').bind(s.userId, id, iv, data, now).run()
    : await env.DB.prepare('UPDATE docs SET rev = rev + 1, iv = ?, data = ?, updated_at = ? WHERE user_id = ? AND id = ? AND rev = ?').bind(iv, data, now, s.userId, id, rev).run();
  if (!res.meta.changes) {
    const cur = await env.DB.prepare('SELECT id, rev, iv, data FROM docs WHERE user_id = ? AND id = ?').bind(s.userId, id).first();
    return json({ error: 'Changed elsewhere', current: cur ? docRow(cur) : null }, 409);
  }
  return json({ rev: rev + 1 });
}

async function deleteDoc(req, env, id) {
  const s = await session(req, env);
  await env.DB.prepare('DELETE FROM docs WHERE user_id = ? AND id = ?').bind(s.userId, id).run();
  return json({ ok: true });
}

async function route(req, env, url) {
  const ip = req.headers.get('cf-connecting-ip') || 'local';
  const { pathname: p } = url;
  const m = req.method;
  if (m !== 'GET') {
    const origin = req.headers.get('origin');
    if (origin && origin !== url.origin) throw new HttpError(403, 'Bad origin');
  }
  if (p === '/api/signup' && m === 'POST') return signup(req, env, ip);
  if (p === '/api/prelogin' && m === 'POST') return prelogin(req, env, ip);
  if (p === '/api/login' && m === 'POST') return login(req, env, ip);
  if (p === '/api/logout' && m === 'POST') return logout(req, env);
  if (p === '/api/me' && m === 'GET') return me(req, env);
  if (p === '/api/sky' && m === 'GET') return sky(req, env);
  if (p === '/api/account/delete' && m === 'POST') return deleteAccount(req, env);
  if (p === '/api/account/key' && m === 'POST') return accountKey(req, env, ip);
  if (p === '/api/account/passphrase' && m === 'POST') return changePassphrase(req, env, ip);
  if (p === '/api/docs' && m === 'GET') return listDocs(req, env, url);
  const d = /^\/api\/doc\/([^/]+)$/.exec(p);
  if (d && DOC_RE.test(d[1])) {
    if (m === 'GET') return getDoc(req, env, d[1]);
    if (m === 'PUT') return putDoc(req, env, d[1]);
    if (m === 'DELETE') return deleteDoc(req, env, d[1]);
  }
  throw new HttpError(404, 'Not found');
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (!url.pathname.startsWith('/api/')) return env.ASSETS.fetch(req);
    try {
      return await route(req, env, url);
    } catch (e) {
      if (e instanceof HttpError) return json({ error: e.message }, e.status);
      console.error(e);
      return json({ error: 'Something went wrong on our side' }, 500);
    }
  },
};
