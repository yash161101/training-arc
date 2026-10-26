const CACHE = 'training-arc-shell-v7';
const SHELL = [
  './',
  'style.css',
  'manifest.webmanifest',
  'js/app.js', 'js/api.js', 'js/crypto.js', 'js/exercises.js', 'js/keystore.js', 'js/logic.js', 'js/store.js', 'js/world.js', 'js/sky.js', 'world/cliff.svg', 'world/yard.svg', 'world/forge.svg', 'world/boulders.svg', 'world/valley.svg', 'world/climb.svg', 'world/dojo.svg',
  'fonts/space-grotesk.woff2', 'fonts/plex-mono-500.woff2', 'fonts/plex-mono-600.woff2', 'js/theme.js', 'icons/icon.svg',
  'icons/icon-192.png', 'icons/apple-touch-icon.png',
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

function fromNetwork(req, ms) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('slow')), ms);
    fetch(req).then((res) => { clearTimeout(timer); resolve(res); }, (err) => { clearTimeout(timer); reject(err); });
  });
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  const url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== self.location.origin || url.pathname.startsWith('/api/')) return;
  const key = req.mode === 'navigate' ? './' : req;
  e.respondWith((async () => {
    const cache = await caches.open(CACHE);
    try {
      const res = await fromNetwork(req, 4000);
      if (res.ok && !res.redirected) cache.put(key, res.clone());
      return res;
    } catch {
      const hit = await cache.match(key, { ignoreSearch: true });
      if (hit) return hit;
      return fetch(req);
    }
  })());
});
