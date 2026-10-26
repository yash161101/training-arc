export const EMPTY_SUMMARY = () => ({
  v: 1, episodes: 0, last: {}, best: {}, hist: {}, boss: {}, recent: [], custom: [],
});

export function metric(ex, s) {
  if (!s || !(s.r > 0)) return 0;
  if (ex.bw) return s.r;
  const w = Number(s.w) || 0;
  return s.r === 1 ? w : w * (1 + s.r / 30);
}

export function compare(ex, you, ghost) {
  if (!ghost) return null;
  const d = metric(ex, you) - metric(ex, ghost);
  if (Math.abs(d) < 0.01) return 'tie';
  return d > 0 ? 'beat' : 'lose';
}

export function fmtKg(w) {
  const n = Number(w) || 0;
  return (Math.round(n * 100) / 100).toString();
}

export function fmtSet(ex, s) {
  if (!s) return '';
  if (ex.bw) return `${s.r} ${ex.id === 'plank' ? 'sec' : 'reps'}`;
  return `${s.r} × ${fmtKg(s.w)} kg`;
}

export function diffText(ex, you, ghost) {
  if (!ghost) return '';
  if (ex.bw || Number(you.w) === Number(ghost.w)) {
    const d = you.r - ghost.r;
    return d === 0 ? 'Level' : (d > 0 ? '+' : '') + d + (ex.id === 'plank' ? ' sec' : d === 1 || d === -1 ? ' rep' : ' reps');
  }
  const r = compare(ex, you, ghost);
  return r === 'beat' ? 'Stronger' : r === 'lose' ? 'Weaker' : 'Even';
}

export function today() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

function daysBetween(a, b) {
  return Math.round((Date.parse(b) - Date.parse(a)) / 86400000);
}

export function bossFor(ex, summary, date = today()) {
  const best = summary.best[ex.id];
  const last = summary.last[ex.id];
  const hist = summary.hist[ex.id] || [];
  if (!best || !last || hist.length < 2 || best.ep === last.ep) return null;
  const lastTop = Math.max(0, ...last.sets.map((s) => metric(ex, s)));
  if (lastTop < best.m * 0.95) return null;
  const fought = summary.boss[ex.id];
  if (fought && daysBetween(fought.date, date) < 7) return null;
  return { best, target: { r: best.r + 1, w: ex.bw ? 0 : best.w } };
}

export function ghostSets(exId, summary) {
  const last = summary.last[exId];
  return last ? last.sets : [];
}

export function newItem(ex, summary) {
  const ghosts = ghostSets(ex.id, summary);
  const count = Math.max(3, ghosts.length);
  const fallback = ghosts[ghosts.length - 1] || { r: ex.bw ? 8 : 10, w: 0 };
  return {
    exId: ex.id,
    sets: Array.from({ length: count }, (_, j) => {
      const g = ghosts[j] || fallback;
      return { r: g.r, w: ex.bw ? 0 : g.w, done: false };
    }),
    boss: null,
  };
}

export function scoreDraft(draft, summary, find) {
  let you = 0, ghost = 0, tie = 0, compared = 0;
  for (const it of draft.items) {
    const ex = find(it.exId);
    if (!ex) continue;
    const gs = ghostSets(it.exId, summary);
    it.sets.forEach((s, j) => {
      if (!s.done) return;
      const r = compare(ex, s, gs[j]);
      if (!r) return;
      compared++;
      if (r === 'beat') you++;
      else if (r === 'lose') ghost++;
      else tie++;
    });
  }
  return { you, ghost, tie, compared };
}

export function buildEpisode(n, draft, summary, find) {
  const date = today();
  const items = [];
  const newBests = [];
  const bosses = [];
  let sets = 0, volume = 0;
  for (const it of draft.items) {
    const ex = find(it.exId);
    if (!ex) continue;
    const gs = ghostSets(it.exId, summary);
    const done = it.sets.filter((s) => s.done).map((s, j) => ({ r: s.r, w: ex.bw ? 0 : Number(s.w) || 0 }));
    const doneWithGhost = [];
    it.sets.forEach((s, j) => {
      if (!s.done) return;
      doneWithGhost.push({ r: s.r, w: ex.bw ? 0 : Number(s.w) || 0, res: compare(ex, s, gs[j]) });
    });
    let boss = null;
    if (it.boss && it.boss.done) {
      const got = { r: it.boss.r, w: ex.bw ? 0 : Number(it.boss.w) || 0 };
      const prev = summary.best[ex.id];
      boss = { target: it.boss.target, got, win: !!prev && metric(ex, got) > prev.m + 0.001, best: prev };
      bosses.push({ ex, boss });
    }
    const all = boss ? [...done, boss.got] : done;
    if (!all.length) continue;
    sets += all.length;
    volume += all.reduce((a, s) => a + (ex.bw ? 0 : s.r * s.w), 0);
    const top = all.reduce((a, s) => (metric(ex, s) > metric(ex, a) ? s : a), all[0]);
    const prevBest = summary.best[ex.id];
    const isBest = !prevBest || metric(ex, top) > prevBest.m + 0.001;
    if (isBest && prevBest && !(boss && boss.win)) newBests.push({ ex, set: top });
    items.push({ exId: ex.id, name: ex.name, bw: ex.bw, sets: doneWithGhost, boss, top, best: isBest });
  }
  const score = scoreDraft(draft, summary, find);
  const win = bosses.find((b) => b.boss.win);
  const lost = bosses.find((b) => !b.boss.win);
  let title;
  if (win) title = `Boss down: ${win.ex.name} ${fmtSet(win.ex, win.boss.got)}`;
  else if (newBests.length) title = `New best: ${newBests[0].ex.name} ${fmtSet(newBests[0].ex, newBests[0].set)}`;
  else if (lost) title = `Boss: ${lost.ex.name} · to be continued`;
  else if (score.compared && score.you > score.ghost) title = `Ghost beaten on ${score.you} of ${score.compared} sets`;
  else if (score.compared && score.ghost > score.you) title = `Ghost wins this one, ${score.ghost} to ${score.you}`;
  else if (score.compared && score.you) title = `Even with your ghost, ${score.you} each`;
  else if (score.compared) title = `Level with your ghost on ${score.tie} sets`;
  else title = `First session: ${items.slice(0, 2).map((i) => i.name).join(', ')}${items.length > 2 ? ` +${items.length - 2}` : ''}`;
  const started = draft.startedAt || Date.now();
  return {
    v: 1, n, date, title, items, score,
    startedAt: started, endedAt: Date.now(),
    minutes: Math.max(1, Math.round((Date.now() - started) / 60000)),
    sets, volume: Math.round(volume),
  };
}

export function applyEpisode(summary, ep, find) {
  const s = JSON.parse(JSON.stringify(summary));
  s.episodes = Math.max(s.episodes, ep.n);
  for (const it of ep.items) {
    const ex = find(it.exId) || { id: it.exId, bw: it.bw };
    const sets = it.sets.map((x) => ({ r: x.r, w: x.w }));
    if (sets.length) s.last[it.exId] = { ep: ep.n, date: ep.date, sets };
    const m = metric(ex, it.top);
    const prev = s.best[it.exId];
    if (!prev || m > prev.m + 0.001) s.best[it.exId] = { m, r: it.top.r, w: it.top.w, ep: ep.n, date: ep.date };
    const h = s.hist[it.exId] || [];
    h.push({ ep: ep.n, d: ep.date, m, r: it.top.r, w: it.top.w });
    s.hist[it.exId] = h.slice(-120);
    if (it.boss) s.boss[it.exId] = { date: ep.date, win: it.boss.win };
  }
  s.recent = [
    { n: ep.n, id: ep.id, date: ep.date, title: ep.title, you: ep.score.you, ghost: ep.score.ghost, ex: ep.items.map((i) => i.exId) },
    ...s.recent.filter((r) => r.n !== ep.n && !(ep.id && r.id === ep.id)),
  ].slice(0, 1000);
  return s;
}

export function templates(summary, limit = 3) {
  const seen = new Set();
  const out = [];
  for (const r of summary.recent) {
    const key = r.ex.join(',');
    if (!r.ex.length || seen.has(key)) continue;
    seen.add(key);
    out.push(r);
    if (out.length >= limit) break;
  }
  return out;
}
