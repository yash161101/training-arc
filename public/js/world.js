import { today } from './logic.js';

const PLACE = { Back: 'pull', Chest: 'push', Shoulders: 'push', Arms: 'arms', Legs: 'legs', Core: 'core' };
const PER = { legs: 3, pull: 3, push: 1, arms: 1, core: 0 };
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
  const places = {};
  for (const p of ['legs', 'pull', 'push', 'arms', 'core']) places[p] = { units: 0, last: '', lastCount: 0 };
  const exercises = [];
  for (const [id, h] of Object.entries(summary.hist)) {
    const ex = find(id);
    if (!ex || !h.length) continue;
    const place = PLACE[ex.group] || 'core';
    const P = places[place];
    let best = 0;
    for (const x of h) {
      P.units += PER[place];
      if (best && x.m > best + 0.001) P.units += 1;
      best = Math.max(best, x.m || 0);
    }
    const d = h[h.length - 1].d;
    if (d > P.last) { P.last = d; P.lastCount = 0; }
    if (d === P.last) P.lastCount++;
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
  for (const p of ['legs', 'push', 'pull', 'arms']) neglect[p] = places[p].last ? Math.max(0, daysBetween(places[p].last, now)) : null;

  const weekAgo = new Date(Date.parse(now) - 7 * DAY).toISOString().slice(0, 10);
  const pl = power(summary, find, null, goodWeeks);
  const bosses = summary.recent.filter((r) => /^Boss down/.test(r.title || '')).map((r) => ({ n: r.n, date: r.date, what: r.title.replace(/^Boss down:\s*/, '') })).reverse();
  const last = summary.recent[0];
  const lastHour = last && last.t ? new Date(last.t).getHours() : null;
  const sinceLast = last && last.t ? (Date.now() - last.t) / 3600000 : last ? daysBetween(last.date, now) * 24 : null;

  return {
    places, legSteps: places.legs.units, lastLegCount: places.legs.lastCount, neglect, exercises, goodWeeks, rank,
    rankName: RANKS[rank][0],
    nextRank: next ? { name: next[0], weeks: next[1] - goodWeeks } : null,
    power: pl, powerWeek: pl - power(summary, find, weekAgo, goodWeeks),
    bosses, bossWins: bosses.length,
    eggs: {
      koi: summary.recent.some((r) => r.perfect),
      pink: !!last && last.date === now && lastHour != null && lastHour >= 4 && lastHour < 6,
      owl: sinceLast != null && sinceLast < 20 && lastHour != null && (lastHour >= 23 || lastHour < 2),
      cat: last ? daysBetween(last.date, now) >= 7 : false,
      hundred: !!last && last.n % 100 === 0 && sinceLast != null && sinceLast < 24,
      over9000: pl > 9000,
    },
  };
}

export function neglectNote(w) {
  const notes = {
    legs: (d) => `No legs for ${d} days. Moss is growing on your stairs.`,
    push: (d) => `No push work for ${d} days. Vines are on your posts.`,
    arms: (d) => `No arm work for ${d} days. The forge has gone cold.`,
    pull: (d) => `No pull work for ${d} days. Moss is on your grips.`,
  };
  let worst = null;
  for (const [p, d] of Object.entries(w.neglect)) if (d != null && d >= 7 && (!worst || d > worst[1])) worst = [p, d];
  return worst ? notes[worst[0]](worst[1]) : '';
}

const show = (root, sel, on) => { const el = root.querySelector(sel); if (el) el.setAttribute('display', on ? 'inline' : 'none'); };
const over = (d, n) => d != null && d >= n;

export function paintValley(root, w, sky, bossWaiting) {
  const night = sky.night;
  root.classList.toggle('is-night', night);
  show(root, '#w-sun', !night);
  show(root, '#w-birds', !night && (sky.weather === 'clear' || sky.weather === 'cloudy'));
  show(root, '#w-warm', !night);
  show(root, '#w-nightsky', night);
  show(root, '#w-night', night);
  show(root, '#w-vwin', night);
  show(root, '#w-dusk', sky.phase === 'dusk' || sky.phase === 'dawn');
  show(root, '#w-pink', w.eggs.pink && !night);
  const shadow = root.querySelector('#w-moonshadow');
  if (shadow) {
    const m = sky.moon;
    shadow.setAttribute('cx', String(Math.round(1980 + (m < 0.5 ? -168 * m : 168 * (1 - m)))));
    shadow.setAttribute('cy', '150');
  }
  show(root, '#w-cloudy', sky.weather === 'cloudy' || sky.weather === 'rain' || sky.weather === 'storm');
  show(root, '#w-rain', sky.weather === 'rain' || sky.weather === 'storm');
  root.classList.toggle('is-storm', sky.weather === 'storm');
  show(root, '#w-fog', sky.weather === 'fog');
  show(root, '#w-snow', sky.weather === 'snow');
  show(root, '#w-diwali', sky.festival === 'diwali');
  show(root, '#w-holi', sky.festival === 'holi');
  show(root, '#w-fireworks', (sky.festival === 'newyear' || w.eggs.hundred) && (night || sky.phase === 'dusk'));
  const s = sky.season;
  show(root, '#w-cb', s === 'spring');
  show(root, '#w-ca', s === 'autumn');
  show(root, '#w-cg', s === 'summer' || s === 'monsoon' || s === 'winter');
  show(root, '#w-leaves', s === 'autumn');
  show(root, '#w-monsoon', s === 'monsoon');
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
  show(root, '#w-koi', w.eggs.koi);
  show(root, '#w-owl', w.eggs.owl && night);
  show(root, '#w-cat', w.eggs.cat);
  show(root, '#w-banner9000', w.eggs.over9000);
}

export function climbState(w, total) {
  const laid = Math.min(w.legSteps, total);
  const d = w.neglect.legs;
  const moss = over(d, 7) ? Math.min(9, laid, Math.floor(d / 2)) : 0;
  const ghost = laid < total ? Math.min(total - laid, Math.max(3, w.lastLegCount * 3)) : 0;
  return { laid, moss, ghost, total };
}

export function paintClimb(root, w, sky) {
  const steps = [...root.querySelectorAll('.c-step')];
  const c = climbState(w, steps.length);
  steps.forEach((el, i) => {
    let k = 'trail';
    if (i < c.laid) k = i >= c.laid - c.moss ? 'laid moss' : 'laid';
    else if (i < c.laid + c.ghost) k = 'ghost';
    el.setAttribute('class', 'c-step ' + k);
  });
  root.querySelectorAll('.c-land').forEach((el) => el.setAttribute('class', 'c-land ' + (+el.dataset.i <= c.laid ? 'on' : 'off')));
  root.classList.toggle('is-night', sky.night);
  show(root, '#c-nightsky', sky.night);
  show(root, '#c-night', sky.night);
  const cur = steps[Math.max(0, c.laid - 1)];
  return { ...c, focusY: cur ? +cur.dataset.y : 1560 };
}

export function placeState(w, key, total, bossWaiting) {
  if (key === 'boulders') return { laid: Math.min(w.bossWins, total), ghost: bossWaiting && w.bossWins < total ? 1 : 0, moss: 0, total };
  const P = w.places[key];
  const laid = Math.min(P.units, total);
  const d = w.neglect[key];
  const moss = key === 'pull' && over(d, 7) ? Math.min(6, laid, Math.floor(d / 2)) : 0;
  const ghost = laid < total ? Math.min(total - laid, Math.max(PER[key], P.lastCount * PER[key])) : 0;
  return { laid, moss, ghost, total };
}

export function paintPlace(root, w, sky, key, bossWaiting) {
  const units = [...root.querySelectorAll('.u')];
  const c = placeState(w, key, units.length, bossWaiting);
  units.forEach((el, i) => {
    let k = 'empty';
    if (i < c.laid) k = i >= c.laid - c.moss ? 'laid moss' : 'laid';
    else if (i < c.laid + c.ghost) k = 'ghost';
    el.setAttribute('class', 'u ' + k);
    const label = el.querySelector('.u-label');
    if (label) label.textContent = w.bosses[i] ? `Ep ${w.bosses[i].n}` : '';
  });
  root.querySelectorAll('.u-land').forEach((el) => el.setAttribute('class', 'u-land ' + (+el.dataset.i <= c.laid ? 'on' : 'off')));
  root.classList.toggle('is-night', sky.night);
  show(root, '#n-night', sky.night);
  show(root, '#n-nightsky', sky.night);
  show(root, '#n-vines', key === 'push' && over(w.neglect.push, 7));
  const cold = key === 'arms' && over(w.neglect.arms, 7);
  show(root, '#n-fire', !cold);
  show(root, '#n-cold', cold);
  const cur = units[Math.max(0, c.laid - 1)];
  return { ...c, focusY: cur ? +cur.dataset.y : null };
}

export function paintDojo(root, w, sky) {
  root.querySelectorAll('.d-plaque').forEach((el) => {
    const i = +el.dataset.i;
    el.setAttribute('class', 'd-plaque ' + (i < w.rank ? 'done' : i === w.rank ? 'on' : 'todo'));
  });
  root.querySelectorAll('.d-scroll').forEach((el) => {
    const ex = w.exercises[+el.dataset.i];
    el.setAttribute('class', 'd-scroll ' + (ex ? 'open' : 'rolled'));
    el.querySelectorAll('.m').forEach((m) => m.setAttribute('display', ex && +m.dataset.k < ex.form ? 'inline' : 'none'));
  });
  show(root, '#d-night', sky.night);
  show(root, '#d-ray', !sky.night);
}
