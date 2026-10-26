import { today } from './logic.js';

const PLACE = { Back: 'pull', Chest: 'push', Shoulders: 'push', Arms: 'arms', Legs: 'legs', Core: 'core' };
export const RANKS = [['Rookie', 0], ['Trainee', 1], ['Fighter', 3], ['Veteran', 6], ['Master', 10], ['Legend', 16]];
export const FORMS = ['First form', 'Second form', 'Third form', 'Fourth form', 'Fifth form'];
export const VETERAN = 3;

const DAY = 86400000;
const daysBetween = (a, b) => Math.round((Date.parse(b) - Date.parse(a)) / DAY);

function weekKey(d) {
  const t = new Date(d + 'T00:00:00Z');
  const back = (t.getUTCDay() + 6) % 7;
  return new Date(t.getTime() - back * DAY).toISOString().slice(0, 10);
}

function power(summary, find, cutoff, goodWeeks) {
  let total = 0;
  for (const [id, h] of Object.entries(summary.hist)) {
    const ex = find(id);
    if (!ex) continue;
    let best = 0;
    for (const x of h) if (!cutoff || x.d <= cutoff) best = Math.max(best, x.m || 0);
    total += ex.bw ? best * 4 : best;
  }
  return Math.round(total * 10) + goodWeeks * 50;
}

export function worldState(summary, find, now = today()) {
  const last = {};
  const exercises = [];
  let legSteps = 0;
  let lastLegCount = 0;
  let lastLegDate = '';
  for (const [id, h] of Object.entries(summary.hist)) {
    const ex = find(id);
    if (!ex || !h.length) continue;
    const place = PLACE[ex.group] || 'core';
    const d = h[h.length - 1].d;
    if (!last[place] || d > last[place]) last[place] = d;
    if (place === 'legs') {
      let best = 0;
      for (const x of h) {
        legSteps += 3;
        if (best && x.m > best + 0.001) legSteps += 1;
        best = Math.max(best, x.m || 0);
      }
      if (d > lastLegDate) { lastLegDate = d; lastLegCount = 0; }
      if (d === lastLegDate) lastLegCount++;
    }
    const n = h.length;
    const form = Math.min(5, 1 + Math.floor((n - 1) / 3));
    exercises.push({ id, name: ex.name, place, sessions: n, form, toNext: form < 5 ? form * 3 + 1 - n : 0 });
  }
  exercises.sort((a, b) => b.sessions - a.sessions || a.name.localeCompare(b.name));

  const weeks = {};
  for (const r of summary.recent) {
    if (!r.date) continue;
    const k = weekKey(r.date);
    (weeks[k] = weeks[k] || new Set()).add(r.date);
  }
  const goodWeeks = Object.values(weeks).filter((s) => s.size >= 3).length;
  let rank = 0;
  RANKS.forEach(([, need], i) => { if (goodWeeks >= need) rank = i; });
  const next = RANKS[rank + 1];

  const neglect = {};
  for (const p of ['legs', 'push', 'pull', 'arms']) neglect[p] = last[p] ? Math.max(0, daysBetween(last[p], now)) : null;

  const weekAgo = new Date(Date.parse(now) - 7 * DAY).toISOString().slice(0, 10);
  const pl = power(summary, find, null, goodWeeks);
  const plBefore = power(summary, find, weekAgo, goodWeeks);

  return {
    legSteps, lastLegCount, neglect, exercises, goodWeeks, rank,
    rankName: RANKS[rank][0],
    nextRank: next ? { name: next[0], weeks: next[1] - goodWeeks } : null,
    power: pl, powerWeek: pl - plBefore,
    bossWins: summary.recent.filter((r) => /^Boss down/.test(r.title || '')).length,
  };
}

export function neglectNote(w) {
  const notes = {
    legs: (d) => `No legs for ${d} days. Moss is growing on your stairs.`,
    push: (d) => `No push work for ${d} days. Vines are on your posts.`,
    arms: (d) => `No arm work for ${d} days. The forge has gone cold.`,
    pull: (d) => `No pull work for ${d} days. The rope is waiting.`,
  };
  let worst = null;
  for (const [p, d] of Object.entries(w.neglect)) if (d != null && d >= 7 && (!worst || d > worst[1])) worst = [p, d];
  return worst ? notes[worst[0]](worst[1]) : '';
}

const show = (root, sel, on) => { const el = root.querySelector(sel); if (el) el.setAttribute('display', on ? 'inline' : 'none'); };
const over = (d, n) => d != null && d >= n;

export function paintValley(root, w, dark, bossWaiting) {
  show(root, '#w-sun', !dark);
  show(root, '#w-birds', !dark);
  show(root, '#w-warm', !dark);
  show(root, '#w-nightsky', dark);
  show(root, '#w-night', dark);
  show(root, '#w-vwin', dark);
  show(root, '#w-moss', over(w.neglect.legs, 7));
  show(root, '#w-gatevines', over(w.neglect.legs, 14));
  show(root, '#w-postvines', over(w.neglect.push, 7));
  const cold = over(w.neglect.arms, 7);
  show(root, '#w-fire', !cold);
  show(root, '#w-coals', !cold);
  show(root, '#w-nightfire', !cold);
  show(root, '#w-floor2', w.rank >= VETERAN);
  show(root, '#w-floor2-ghost', w.rank < VETERAN);
  show(root, '#w-split1', w.bossWins >= 1);
  show(root, '#w-split2', w.bossWins >= 2);
  show(root, '#w-bosswait', !!bossWaiting);
}

export function climbState(w, total) {
  const laid = Math.min(w.legSteps, total);
  const d = w.neglect.legs;
  const moss = over(d, 7) ? Math.min(9, laid, Math.floor(d / 2)) : 0;
  const ghost = laid < total ? Math.min(total - laid, Math.max(3, w.lastLegCount * 3)) : 0;
  return { laid, moss, ghost, total };
}

export function paintClimb(root, w, dark) {
  const steps = [...root.querySelectorAll('.c-step')];
  const c = climbState(w, steps.length);
  steps.forEach((el, i) => {
    let k = 'trail';
    if (i < c.laid) k = i >= c.laid - c.moss ? 'laid moss' : 'laid';
    else if (i < c.laid + c.ghost) k = 'ghost';
    el.setAttribute('class', 'c-step ' + k);
  });
  let nextLanding = null;
  root.querySelectorAll('.c-land').forEach((el) => {
    const at = +el.dataset.i;
    const on = at <= c.laid;
    el.setAttribute('class', 'c-land ' + (on ? 'on' : 'off'));
    if (!on && (nextLanding == null || at < nextLanding)) nextLanding = at;
  });
  root.classList.toggle('is-night', dark);
  show(root, '#c-nightsky', dark);
  show(root, '#c-night', dark);
  const cur = steps[Math.max(0, c.laid - 1)];
  return { ...c, nextLanding, focusY: cur ? +cur.dataset.y : 1560 };
}

export function paintDojo(root, w, dark) {
  root.querySelectorAll('.d-plaque').forEach((el) => {
    const i = +el.dataset.i;
    el.setAttribute('class', 'd-plaque ' + (i < w.rank ? 'done' : i === w.rank ? 'on' : 'todo'));
  });
  root.querySelectorAll('.d-scroll').forEach((el) => {
    const ex = w.exercises[+el.dataset.i];
    el.setAttribute('class', 'd-scroll ' + (ex ? 'open' : 'rolled'));
    el.querySelectorAll('.m').forEach((m) => m.setAttribute('display', ex && +m.dataset.k < ex.form ? 'inline' : 'none'));
  });
  show(root, '#d-night', dark);
  show(root, '#d-ray', !dark);
}
