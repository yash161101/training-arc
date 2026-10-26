import {
  session, restore, join, enter, lock, destroy, loadSummary, saveEpisode, addCustom,
  getEpisode, loadDraft, saveDraft, clearDraft, exportAll, onSync, syncNow, pendingCount, retryDraft,
} from './store.js';
import { oathProblem } from './crypto.js';
import { GROUPS, allExercises, findExercise } from './exercises.js';
import {
  compare, fmtSet, fmtKg, diffText, bossFor, ghostSets, newItem, scoreDraft, buildEpisode, templates, metric,
} from './logic.js';

const app = document.getElementById('app');

const st = {
  view: 'boot',
  authTab: 'join',
  lastName: '',
  err: '',
  busy: '',
  draft: null,
  saveStatus: '',
  picker: { sel: [], q: '', group: 'All', mode: 'new', custom: false },
  episode: null,
  episodeFrom: 'home',
  exDetail: null,
  confirmDelete: false,
  showOath: false,
};

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const custom = () => (session.summary && session.summary.custom) || [];
const find = (id) => findExercise(id, custom());
const sum = () => session.summary;
const nextEp = () => (sum() ? sum().episodes + 1 : 1);

function niceDate(d) {
  if (!d) return '';
  return new Date(d + 'T00:00:00').toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short' });
}

const ICON = {
  gear: '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><circle cx="12" cy="12" r="3.2"></circle><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"></path></svg>',
  back: '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" aria-hidden="true"><path d="M15 5l-7 7 7 7"></path></svg>',
  x: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"></path></svg>',
  check: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" aria-hidden="true"><path d="M5 12l5 5L20 7"></path></svg>',
};

function bar(title, { back = null, right = '' } = {}) {
  return `<header class="bar">
    ${back ? `<button class="icon-btn" data-act="go" data-view="${back}" aria-label="Back">${ICON.back}</button>` : '<span class="logo-sm">Training Arc</span>'}
    ${title ? `<span class="bar-title">${esc(title)}</span>` : '<span></span>'}
    ${right || '<span class="icon-spacer"></span>'}
  </header>`;
}

function errBox() {
  return st.err ? `<p class="err" role="alert">${esc(st.err)}</p>` : '';
}

function viewBoot() {
  return `<main class="center"><div class="sun big"></div><h1 class="logo">Training<br>Arc</h1></main>`;
}

function viewAuth() {
  const join = st.authTab === 'join';
  const t = st.showOath ? 'text' : 'password';
  return `<main class="auth">
    <section class="auth-hero">
      <div class="sun"></div>
      <h1 class="logo">Training<br>Arc</h1>
      <p class="tag">Every set, you race who you were.</p>
    </section>
    <div class="tabs" role="tablist">
      <button class="tab ${join ? 'on' : ''}" data-act="tab" data-tab="join" role="tab" aria-selected="${join}">Join</button>
      <button class="tab ${join ? '' : 'on'}" data-act="tab" data-tab="return" role="tab" aria-selected="${!join}">Return</button>
    </div>
    ${join ? `<form class="card form" data-form="join" autocomplete="on" novalidate>
      <label class="field"><span>Invite code</span>
        <input name="invite" autocomplete="off" autocapitalize="none" spellcheck="false" maxlength="64" required></label>
      <label class="field"><span>Fighter name</span>
        <input name="name" autocomplete="username" autocapitalize="none" spellcheck="false" maxlength="20" placeholder="e.g. batman" required></label>
      <label class="field"><span>Passphrase</span>
        <input name="oath" type="${t}" autocomplete="new-password" spellcheck="false" placeholder="At least 10 characters" required></label>
      <p class="hint">Pick something you'll remember. It encrypts your data, so it can't be reset.</p>
      <label class="field"><span>Confirm passphrase</span>
        <input name="oath2" type="${t}" autocomplete="new-password" spellcheck="false" required></label>
      <button type="button" class="link" data-act="show-oath">${st.showOath ? 'Hide' : 'Show'}</button>
      <label class="check"><input type="checkbox" name="keep" checked><span>Stay signed in on this phone</span></label>
      <label class="check"><input type="checkbox" name="ok"><span>I understand: if I forget my passphrase, my data can't be recovered.</span></label>
      ${errBox()}
      <button class="btn red" type="submit" ${st.busy ? 'disabled' : ''}>${st.busy ? esc(st.busy) : 'Start training'}</button>
    </form>` : `<form class="card form" data-form="return" autocomplete="on" novalidate>
      <label class="field"><span>Fighter name</span>
        <input name="name" autocomplete="username" autocapitalize="none" spellcheck="false" maxlength="20" value="${esc(st.lastName)}" required></label>
      <label class="field"><span>Passphrase</span>
        <input name="oath" type="${t}" autocomplete="current-password" spellcheck="false" required></label>
      <button type="button" class="link" data-act="show-oath">${st.showOath ? 'Hide' : 'Show'}</button>
      <label class="check"><input type="checkbox" name="keep" checked><span>Stay signed in on this phone</span></label>
      ${errBox()}
      <button class="btn red" type="submit" ${st.busy ? 'disabled' : ''}>${st.busy ? esc(st.busy) : 'Sign in'}</button>
    </form>`}
  </main>`;
}

function bossLine(ex, b) {
  return `${esc(ex.name)}. Your best: ${esc(fmtSet(ex, b.best))} (Ep. ${b.best.ep})`;
}

function viewHome() {
  const s = sum();
  const tpl = templates(s);
  const waiting = [];
  const seen = new Set();
  for (const t of tpl) for (const id of t.ex) {
    if (seen.has(id)) continue;
    seen.add(id);
    const ex = find(id);
    const b = ex && bossFor(ex, s);
    if (b) waiting.push(bossLine(ex, b));
  }
  const last = s.recent[0];
  return `${bar('', { right: `<span class="bar-right">${syncChip()}<button class="icon-btn" data-act="go" data-view="settings" aria-label="Settings">${ICON.gear}</button></span>` })}
  <main class="home">
    <section class="hero">
      <div class="sun"></div>
      <span class="kicker">Next episode</span>
      <div class="ep-num">Ep. ${nextEp()}</div>
    </section>
    ${st.draft ? `<section class="card resume">
      <div><span class="kicker">Unfinished</span><h2>${esc(st.draft.items.map((i) => (find(i.exId) || {}).name).filter(Boolean).slice(0, 2).join(', ') || 'Workout')}</h2></div>
      <div class="row-btns"><button class="btn red" data-act="resume">Resume</button><button class="btn outline" data-act="discard">Discard</button></div>
    </section>` : ''}
    ${waiting.length ? `<section class="boss-banner">
      <span class="boss-k">Boss waiting</span>
      ${waiting.slice(0, 2).map((w) => `<p>${w}</p>`).join('')}
    </section>` : ''}
    <section class="start">
      ${tpl.map((t) => {
        const names = t.ex.map((id) => (find(id) || {}).name).filter(Boolean);
        return `<button class="tile" data-act="repeat" data-n="${t.n}">
          <span class="tile-k">Repeat Ep. ${t.n}</span>
          <span class="tile-t">${esc(names.slice(0, 2).join(', '))}${names.length > 2 ? ` +${names.length - 2}` : ''}</span>
        </button>`;
      }).join('')}
      <button class="btn ${tpl.length ? 'black' : 'red'}" data-act="new">New session</button>
    </section>
    ${last ? `<section class="last">
      <span class="kicker">Last episode</span>
      <button class="ep-row" data-act="open-ep" data-n="${last.n}" data-from="home">
        <span class="ep-row-n">${last.n}</span>
        <span class="ep-row-body"><b>${esc(last.title)}</b><small>${esc(niceDate(last.date))}</small></span>
      </button>
    </section>` : `<p class="note">Your first episode starts when you log your first set.</p>`}
    <nav class="links">
      <button class="btn outline" data-act="go" data-view="history">History</button>
      <button class="btn outline" data-act="go" data-view="progress">Progress</button>
    </nav>
  </main>`;
}

function viewPicker() {
  const p = st.picker;
  const q = p.q.trim().toLowerCase();
  const list = allExercises(custom()).filter((e) => (p.group === 'All' || e.group === p.group) && (!q || e.name.toLowerCase().includes(q)));
  const done = sum().last;
  const count = p.sel.length;
  const back = p.mode === 'add' ? 'workout' : 'home';
  return `${bar(p.mode === 'add' ? 'Add exercise' : 'Pick exercises', { back })}
  <main class="picker">
    <input class="search" data-field="q" placeholder="Search exercises" value="${esc(p.q)}" autocomplete="off" aria-label="Search exercises">
    <div class="chips">
      ${['All', ...GROUPS].map((g) => `<button class="chip ${p.group === g ? 'on' : ''}" data-act="group" data-g="${g}">${g}</button>`).join('')}
    </div>
    <ul class="ex-list">
      ${list.map((e) => {
        const on = p.sel.includes(e.id);
        return `<li><button class="ex-pick ${on ? 'on' : ''}" data-act="pick" data-id="${esc(e.id)}" aria-pressed="${on}">
          <span><b>${esc(e.name)}</b><small>${esc(e.group)}${e.bw ? ' · bodyweight' : ''}${done[e.id] ? ' · has a ghost' : ''}</small></span>
          <span class="tick">${on ? ICON.check : ''}</span>
        </button></li>`;
      }).join('') || '<li class="note">Nothing found.</li>'}
    </ul>
    ${p.custom ? `<form class="card form" data-form="custom">
      <label class="field"><span>Exercise name</span><input name="cname" maxlength="40" required></label>
      <label class="field"><span>Muscle group</span><select name="cgroup">${GROUPS.map((g) => `<option>${g}</option>`).join('')}</select></label>
      <label class="check"><input type="checkbox" name="cbw"><span>Bodyweight (count reps only)</span></label>
      ${errBox()}
      <div class="row-btns"><button class="btn black" type="submit">Add</button><button class="btn outline" type="button" data-act="custom-off">Cancel</button></div>
    </form>` : '<button class="link" data-act="custom-on">+ Add your own exercise</button>'}
  </main>
  <footer class="sticky"><button class="btn red" data-act="start" ${count ? '' : 'disabled'}>${p.mode === 'add' ? `Add ${count || ''} to workout` : `Start Ep. ${nextEp()}${count ? ` · ${count}` : ''}`}</button></footer>`;
}

function stamp(res, ex, s, g) {
  if (res === 'beat') return `<span class="stamp beat">Beat ${esc(diffText(ex, s, g))}</span>`;
  if (res === 'tie') return '<span class="stamp tie">Tied</span>';
  if (res === 'lose') return `<span class="stamp lose">Ghost ${esc(diffText(ex, g, s).replace('Stronger', 'wins'))}</span>`;
  return '<span class="stamp logged">Logged</span>';
}

function setInputs(i, j, s, ex, field = '') {
  return `<div class="inputs">
    <div class="stepper">
      <button class="step" data-act="rep" data-i="${i}" data-j="${j}" data-d="-1" aria-label="One fewer">−</button>
      <input class="num" data-field="r${field}" data-i="${i}" data-j="${j}" inputmode="numeric" value="${esc(s.r)}" aria-label="Reps">
      <button class="step" data-act="rep" data-i="${i}" data-j="${j}" data-d="1" aria-label="One more">+</button>
    </div>
    ${ex.bw ? `<span class="unit">${ex.id === 'plank' ? 'sec' : 'reps'}</span>` : `<label class="kg"><input class="num" data-field="w${field}" data-i="${i}" data-j="${j}" inputmode="decimal" value="${esc(fmtKg(s.w))}" aria-label="Weight in kg"><span class="unit">kg</span></label>`}
  </div>`;
}

function viewWorkout() {
  const d = st.draft;
  const s = sum();
  const sc = scoreDraft(d, s, find);
  const status = { saving: 'Saving…', saved: 'Saved', local: 'Saved on this phone. Will retry.' }[st.saveStatus] || '';
  return `<header class="wbar">
    <button class="icon-btn" data-act="leave" aria-label="Back to home">${ICON.back}</button>
    <div class="wbar-mid"><span class="kicker">Ep. ${nextEp()}</span><span class="timer" id="timer">00:00</span></div>
    <div class="score"><span class="you">You ${sc.you}</span><span class="gh">Ghost ${sc.ghost}</span></div>
  </header>
  <p class="savestate" aria-live="polite">${esc(status)}</p>
  <main class="workout">
    ${d.items.map((it, i) => {
      const ex = find(it.exId);
      if (!ex) return '';
      const gs = ghostSets(ex.id, s);
      const lastEp = s.last[ex.id] && s.last[ex.id].ep;
      const b = bossFor(ex, s);
      return `<section class="ex card">
        <div class="ex-head">
          <div><h3>${esc(ex.name)}</h3><span class="sub">${lastEp ? `Ghost from Ep. ${lastEp}` : 'First time. No ghost yet.'}</span></div>
          <button class="icon-btn small" data-act="rm-ex" data-i="${i}" aria-label="Remove ${esc(ex.name)}">${ICON.x}</button>
        </div>
        ${it.sets.map((set, j) => {
          const g = gs[j];
          const res = set.done ? compare(ex, set, g) : null;
          if (set.done) return `<div class="set done">
            <span class="n">${j + 1}</span>
            <span class="val">${esc(fmtSet(ex, set))}</span>
            <button class="stamp-btn" data-act="undo" data-i="${i}" data-j="${j}" aria-label="Set ${j + 1} done. Tap to edit.">${stamp(res, ex, set, g)}</button>
          </div>`;
          return `<div class="set">
            <span class="n">${j + 1}</span>
            <div class="set-body">
              <span class="ghost-line">${g ? `Ghost <b>${esc(fmtSet(ex, g))}</b>` : 'No ghost'}</span>
              ${setInputs(i, j, set, ex)}
            </div>
            <button class="done-btn" data-act="done" data-i="${i}" data-j="${j}">Done</button>
          </div>`;
        }).join('')}
        <div class="ex-foot">
          <button class="link" data-act="add-set" data-i="${i}">+ Set</button>
          ${it.sets.length > 1 && !it.sets[it.sets.length - 1].done ? `<button class="link" data-act="rm-set" data-i="${i}">− Set</button>` : ''}
        </div>
        ${b ? bossBox(i, it, ex, b) : ''}
      </section>`;
    }).join('')}
    <button class="btn outline" data-act="add-ex">+ Add exercise</button>
    ${errBox()}
  </main>
  <footer class="sticky"><button class="btn red" data-act="finish" ${st.busy ? 'disabled' : ''}>${st.busy ? esc(st.busy) : 'Finish episode'}</button></footer>`;
}

function bossBox(i, it, ex, b) {
  const bo = it.boss;
  const head = `<div class="boss-head"><span class="boss-k">Boss</span><span>Your best: <b>${esc(fmtSet(ex, b.best))}</b> · Ep. ${b.best.ep}</span></div>`;
  if (!bo) return `<div class="boss">${head}
    <p class="boss-p">One all-out set. Beat ${esc(fmtSet(ex, b.best))} and your new best becomes the next boss.</p>
    <button class="btn black" data-act="boss" data-i="${i}">Fight: ${esc(fmtSet(ex, b.target))}</button>
  </div>`;
  if (bo.done) {
    const win = metric(ex, bo) > b.best.m + 0.001;
    return `<div class="boss ${win ? 'won' : 'lost'}">${head}
      <button class="boss-result" data-act="boss-undo" data-i="${i}" aria-label="Boss result. Tap to edit.">
        <span class="boss-big">${win ? 'Boss defeated' : 'To be continued'}</span>
        <span>${esc(fmtSet(ex, bo))}</span>
      </button>
    </div>`;
  }
  return `<div class="boss">${head}
    <div class="set boss-set">
      <span class="n">B</span>
      <div class="set-body">${setInputs(i, -1, bo, ex, 'b')}</div>
      <button class="done-btn" data-act="boss-done" data-i="${i}">Done</button>
    </div>
    <button class="link" data-act="boss-skip" data-i="${i}">Not today</button>
  </div>`;
}

function syncNote(ep) {
  const pending = ep.id && session.outbox.some((op) => op.id === ep.id);
  return `<p class="sync-note ${pending ? 'wait' : 'ok'}">${pending ? 'Saved on this phone. Syncs when you’re online.' : 'Saved and synced.'}</p>`;
}

function viewEpisode() {
  const ep = st.episode;
  const entry = ep.id && sum().recent.find((r) => r.id === ep.id);
  if (entry) ep.n = entry.n;
  const back = st.episodeFrom === 'finish' ? null : st.episodeFrom;
  return `${back ? bar('', { back }) : ''}
  <main class="episode">
    <section class="ep-card ${back ? '' : 'reveal'}">
      <div class="sun"></div>
      <span class="kicker">Episode</span>
      <div class="ep-big">${ep.n}</div>
      <h1 class="ep-title">${esc(ep.title)}</h1>
      <span class="ep-date">${esc(niceDate(ep.date))}</span>
      <div class="stats">
        <div><b>${ep.minutes}</b><span>min</span></div>
        <div><b>${ep.sets}</b><span>sets</span></div>
        <div><b>${ep.score.you}–${ep.score.ghost}</b><span>vs ghost</span></div>
        <div><b>${ep.volume}</b><span>kg moved</span></div>
      </div>
      ${syncNote(ep)}
    </section>
    <section class="ep-items">
      ${ep.items.map((it) => {
        const ex = { id: it.exId, name: it.name, bw: it.bw };
        return `<div class="ep-item">
          <div class="ep-item-head"><b>${esc(it.name)}</b>${it.best && !(it.boss && it.boss.win) && it.sets.length ? '<span class="badge">New best</span>' : ''}</div>
          <div class="ep-sets">${it.sets.map((x) => `<span class="pill ${x.res || ''}">${esc(fmtSet(ex, x))}</span>`).join('')}</div>
          ${it.boss ? `<p class="ep-boss ${it.boss.win ? 'won' : ''}">${it.boss.win ? 'Boss defeated' : 'Boss: to be continued'} · ${esc(fmtSet(ex, it.boss.got))}</p>` : ''}
        </div>`;
      }).join('')}
    </section>
    <button class="btn red" data-act="go" data-view="${back || 'home'}">${back ? 'Back' : 'Done'}</button>
  </main>`;
}

function viewHistory() {
  const r = sum().recent;
  return `${bar('History', { back: 'home' })}
  <main class="list-page">
    ${r.length ? r.map((e) => `<button class="ep-row" data-act="open-ep" data-n="${e.n}" data-from="history">
      <span class="ep-row-n">${e.n}</span>
      <span class="ep-row-body"><b>${esc(e.title)}</b><small>${esc(niceDate(e.date))}${e.you + e.ghost ? ` · You ${e.you}, ghost ${e.ghost}` : ''}</small></span>
    </button>`).join('') : '<p class="note">No episodes yet. Finish a workout and it shows up here.</p>'}
    ${errBox()}
  </main>`;
}

function spark(points, w, h) {
  if (points.length < 2) return '';
  const min = Math.min(...points), max = Math.max(...points);
  const span = max - min || 1;
  const xy = points.map((p, k) => `${((k / (points.length - 1)) * (w - 8) + 4).toFixed(1)},${(h - 4 - ((p - min) / span) * (h - 8)).toFixed(1)}`);
  const lastPt = xy[xy.length - 1].split(',');
  return `<svg class="spark" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" aria-hidden="true">
    <polyline points="${xy.join(' ')}" fill="none" stroke="#141414" stroke-width="2.5" stroke-linejoin="round"></polyline>
    <circle cx="${lastPt[0]}" cy="${lastPt[1]}" r="4" fill="#D2402C"></circle>
  </svg>`;
}

function viewProgress() {
  const s = sum();
  const ids = Object.keys(s.hist).sort((a, b) => s.hist[b].length - s.hist[a].length);
  return `${bar('Progress', { back: 'home' })}
  <main class="list-page">
    ${ids.length ? ids.map((id) => {
      const ex = find(id) || { id, name: id, bw: false };
      const h = s.hist[id];
      return `<button class="prog-row" data-act="ex-detail" data-id="${esc(id)}">
        <span class="prog-body"><b>${esc(ex.name)}</b><small>Best ${esc(fmtSet(ex, s.best[id]))} · ${h.length} session${h.length === 1 ? '' : 's'}</small></span>
        ${spark(h.map((x) => x.m), 96, 40)}
      </button>`;
    }).join('') : '<p class="note">Log a few sessions and your progress shows up here.</p>'}
  </main>`;
}

function viewExercise() {
  const s = sum();
  const id = st.exDetail;
  const ex = find(id) || { id, name: id, bw: false };
  const h = s.hist[id] || [];
  return `${bar(ex.name, { back: 'progress' })}
  <main class="list-page">
    <section class="card ex-chart">
      <span class="kicker">${ex.bw ? 'Top set, reps' : 'Top set, estimated 1-rep max'}</span>
      ${spark(h.map((x) => x.m), 320, 140) || '<p class="note">One more session and a line appears.</p>'}
      <p class="best">Best: <b>${esc(fmtSet(ex, s.best[id]))}</b> · Ep. ${s.best[id] ? s.best[id].ep : '–'}</p>
    </section>
    ${h.slice().reverse().map((x) => `<div class="hist-row"><span>Ep. ${x.ep}</span><span>${esc(niceDate(x.d))}</span><b>${esc(fmtSet(ex, x))}</b></div>`).join('')}
  </main>`;
}

function viewSettings() {
  return `${bar('Settings', { back: 'home' })}
  <main class="list-page settings">
    <section class="card">
      <span class="kicker">Fighter</span>
      <h2>${esc(session.name)}</h2>
      <p class="hint">Everything you log is encrypted on this phone with a key only your passphrase can unlock, before it's saved. The server stores scrambled data it can't read.</p>
    </section>
    <p class="remembered ${session.remembered ? 'ok' : ''}">${session.remembered ? 'This phone stays signed in.' : 'This phone won’t stay signed in. Lock, then sign in with “Stay signed in” ticked.'}</p>
    <button class="btn black" data-act="lock">Lock this phone</button>
    <p class="hint">Signs out here and forgets the key. You'll need your passphrase to get back in.</p>
    <button class="btn outline" data-act="export">Download my data</button>
    <p class="hint">A readable copy of everything you've logged, as a file.</p>
    ${st.confirmDelete ? `<form class="card form danger" data-form="delete">
      <p><b>Delete your account and every episode.</b> This can't be undone.</p>
      <label class="field"><span>Enter your passphrase to confirm</span><input name="oath" type="password" autocomplete="current-password" required></label>
      ${errBox()}
      <div class="row-btns"><button class="btn red" type="submit" ${st.busy ? 'disabled' : ''}>${st.busy ? esc(st.busy) : 'Delete forever'}</button><button class="btn outline" type="button" data-act="delete-off">Cancel</button></div>
    </form>` : `<button class="link danger" data-act="delete-on">Delete my account</button>${errBox()}`}
    <p class="hint">Version ${esc(st.version || 'local')}</p>
  </main>`;
}

const VIEWS = {
  boot: viewBoot, auth: viewAuth, home: viewHome, picker: viewPicker, workout: viewWorkout,
  episode: viewEpisode, history: viewHistory, progress: viewProgress, exercise: viewExercise, settings: viewSettings,
};

let lastView = '';

function render() {
  const sameView = lastView === st.view;
  const formVals = sameView ? [...app.querySelectorAll('form [name]')].map((x) => [x.name, x.type === 'checkbox' ? x.checked : x.value]) : [];
  const a = document.activeElement;
  const keep = a && a.dataset && a.dataset.field
    ? { f: a.dataset.field, i: a.dataset.i, j: a.dataset.j, s: a.selectionStart, e: a.selectionEnd }
    : null;
  app.innerHTML = VIEWS[st.view]();
  lastView = st.view;
  formVals.forEach(([n, val]) => {
    const x = app.querySelector(`form [name="${n}"]`);
    if (!x) return;
    if (x.type === 'checkbox') x.checked = val;
    else x.value = val;
  });
  if (keep) {
    let sel = `[data-field="${keep.f}"]`;
    if (keep.i != null) sel += `[data-i="${keep.i}"]`;
    if (keep.j != null) sel += `[data-j="${keep.j}"]`;
    const el = app.querySelector(sel);
    if (el) {
      el.focus();
      try { el.setSelectionRange(keep.s, keep.e); } catch {}
    }
  }
  tick();
}

function go(view) {
  st.view = view;
  st.err = '';
  st.confirmDelete = false;
  render();
  window.scrollTo(0, 0);
}

function stampOverlay(text) {
  const el = document.createElement('div');
  el.className = 'stamp-overlay';
  el.innerHTML = `<span>${esc(text)}</span>`;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 1300);
}

function tick() {
  const el = document.getElementById('timer');
  if (!el || !st.draft) return;
  const secs = Math.max(0, Math.floor((Date.now() - st.draft.startedAt) / 1000));
  const h = Math.floor(secs / 3600), m = Math.floor((secs % 3600) / 60), s = secs % 60;
  el.textContent = (h ? h + ':' + String(m).padStart(2, '0') : String(m).padStart(2, '0')) + ':' + String(s).padStart(2, '0');
}
setInterval(tick, 1000);

function persist() {
  saveDraft(st.draft, (status) => {
    st.saveStatus = status;
    const el = app.querySelector('.savestate');
    if (el) el.textContent = { saving: 'Saving…', saved: 'Saved', local: 'Saved on this phone. Will retry.' }[status] || '';
  });
}

function startWorkout(ids) {
  const items = ids.map((id) => find(id)).filter(Boolean).map((ex) => newItem(ex, sum()));
  if (!items.length) return;
  st.draft = { startedAt: Date.now(), items };
  persist();
  go('workout');
}

function setAt(i, j) {
  const it = st.draft.items[+i];
  return +j === -1 ? it.boss : it.sets[+j];
}

async function enterApp() {
  st.view = 'boot';
  render();
  try {
    await loadSummary();
    st.draft = await loadDraft();
  } catch (e) {
    st.err = e.message;
  }
  go('home');
}

const actions = {
  'tab': (el) => { st.authTab = el.dataset.tab; st.err = ''; render(); },
  'show-oath': () => { st.showOath = !st.showOath; render(); },
  'go': (el) => go(el.dataset.view),
  'new': () => { st.picker = { sel: [], q: '', group: 'All', mode: 'new', custom: false }; go('picker'); },
  'repeat': (el) => { const t = sum().recent.find((r) => r.n === +el.dataset.n); if (t) startWorkout(t.ex); },
  'resume': () => go('workout'),
  'discard': async () => { if (!confirm('Discard this unfinished workout?')) return; await clearDraft(); st.draft = null; render(); },
  'group': (el) => { st.picker.group = el.dataset.g; render(); },
  'pick': (el) => { const p = st.picker; const id = el.dataset.id; p.sel = p.sel.includes(id) ? p.sel.filter((x) => x !== id) : [...p.sel, id]; render(); },
  'custom-on': () => { st.picker.custom = true; st.err = ''; render(); },
  'custom-off': () => { st.picker.custom = false; st.err = ''; render(); },
  'start': () => {
    const p = st.picker;
    if (!p.sel.length) return;
    if (p.mode === 'add') {
      p.sel.forEach((id) => { const ex = find(id); if (ex && !st.draft.items.some((x) => x.exId === id)) st.draft.items.push(newItem(ex, sum())); });
      persist();
      go('workout');
    } else startWorkout(p.sel);
  },
  'leave': () => go('home'),
  'add-ex': () => { st.picker = { sel: [], q: '', group: 'All', mode: 'add', custom: false }; go('picker'); },
  'rm-ex': (el) => { const it = st.draft.items[+el.dataset.i]; if (it.sets.some((s) => s.done) && !confirm('Remove this exercise and its sets?')) return; st.draft.items.splice(+el.dataset.i, 1); persist(); render(); },
  'rep': (el) => { const s = setAt(el.dataset.i, el.dataset.j); s.r = Math.max(0, (parseInt(s.r, 10) || 0) + +el.dataset.d); persist(); render(); },
  'done': (el) => { const s = setAt(el.dataset.i, el.dataset.j); if (!(s.r > 0)) { st.err = 'Add at least 1 rep.'; render(); return; } st.err = ''; s.done = true; persist(); render(); },
  'undo': (el) => { setAt(el.dataset.i, el.dataset.j).done = false; persist(); render(); },
  'add-set': (el) => { const it = st.draft.items[+el.dataset.i]; const prev = it.sets[it.sets.length - 1] || { r: 10, w: 0 }; it.sets.push({ r: prev.r, w: prev.w, done: false }); persist(); render(); },
  'rm-set': (el) => { const it = st.draft.items[+el.dataset.i]; if (it.sets.length > 1 && !it.sets[it.sets.length - 1].done) it.sets.pop(); persist(); render(); },
  'boss': (el) => { const it = st.draft.items[+el.dataset.i]; const ex = find(it.exId); const b = bossFor(ex, sum()); it.boss = { target: b.target, r: b.target.r, w: b.target.w, done: false }; persist(); render(); },
  'boss-done': (el) => { const it = st.draft.items[+el.dataset.i]; if (!(it.boss.r > 0)) return; it.boss.done = true; persist(); render(); },
  'boss-undo': (el) => { st.draft.items[+el.dataset.i].boss.done = false; persist(); render(); },
  'boss-skip': (el) => { st.draft.items[+el.dataset.i].boss = null; persist(); render(); },
  'finish': async () => {
    const d = st.draft;
    const any = d.items.some((it) => it.sets.some((s) => s.done) || (it.boss && it.boss.done));
    if (!any) { st.err = 'Log at least one set first.'; render(); return; }
    const open = d.items.reduce((a, it) => a + it.sets.filter((s) => !s.done).length, 0);
    if (open && !confirm(`${open} set${open === 1 ? ' is' : 's are'} not done. Finish anyway?`)) return;
    st.busy = 'Saving episode…';
    st.err = '';
    render();
    try {
      const ep = await saveEpisode((n) => buildEpisode(n, d, sum(), find));
      await clearDraft();
      st.draft = null;
      st.episode = ep;
      st.episodeFrom = 'finish';
      st.busy = '';
      go('episode');
    } catch (e) {
      st.busy = '';
      st.err = `Not saved yet: ${e.message} Your workout is safe on this phone. Try again.`;
      render();
    }
  },
  'open-ep': async (el) => {
    st.err = '';
    try {
      st.episode = await getEpisode(+el.dataset.n);
      st.episodeFrom = el.dataset.from === 'history' ? 'history' : 'home';
      go('episode');
    } catch (e) {
      st.err = e.message;
      render();
    }
  },
  'ex-detail': (el) => { st.exDetail = el.dataset.id; go('exercise'); },
  'lock': async () => {
    if (pendingCount()) await syncNow();
    const left = pendingCount();
    if (left && !confirm(`${left} episode${left === 1 ? ' hasn\u2019t' : 's haven\u2019t'} synced yet. Locking now deletes ${left === 1 ? 'it' : 'them'} from this phone. Lock anyway?`)) return;
    await lock(); st.draft = null; st.authTab = 'return'; st.lastName = ''; go('auth');
  },
  'export': async () => {
    try {
      const data = await exportAll();
      const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' }));
      const a = document.createElement('a');
      a.href = url;
      a.download = `training-arc-${session.name}-${new Date().toISOString().slice(0, 10)}.json`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 5000);
    } catch (e) {
      st.err = e.message;
      render();
    }
  },
  'delete-on': () => { st.confirmDelete = true; st.err = ''; render(); },
  'delete-off': () => { st.confirmDelete = false; st.err = ''; render(); },
};

app.addEventListener('click', (e) => {
  const el = e.target.closest('[data-act]');
  if (!el || el.disabled) return;
  const fn = actions[el.dataset.act];
  if (fn) {
    e.preventDefault();
    fn(el, e);
  }
});

app.addEventListener('input', (e) => {
  const el = e.target;
  const f = el.dataset && el.dataset.field;
  if (!f) return;
  if (f === 'q') {
    st.picker.q = el.value;
    render();
    return;
  }
  const s = setAt(el.dataset.i, el.dataset.j);
  if (f.startsWith('r')) s.r = Math.max(0, parseInt(el.value.replace(/\D/g, ''), 10) || 0);
  if (f.startsWith('w')) {
    const v = parseFloat(el.value.replace(',', '.'));
    s.w = Number.isFinite(v) && v >= 0 ? Math.min(v, 1000) : 0;
    if (+el.dataset.j >= 0) {
      const it = st.draft.items[+el.dataset.i];
      it.sets.forEach((x, k) => { if (k > +el.dataset.j && !x.done) x.w = s.w; });
    }
  }
  persist();
});

app.addEventListener('change', (e) => {
  if (e.target.dataset && e.target.dataset.field && e.target.dataset.field !== 'q') render();
});

app.addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = e.target;
  const kind = form.dataset.form;
  const v = (n) => (form.elements[n] ? form.elements[n].value : '');
  const c = (n) => !!(form.elements[n] && form.elements[n].checked);
  st.err = '';
  if (kind === 'join' || kind === 'return') {
    const name = v('name').trim().toLowerCase();
    const oath = v('oath');
    st.lastName = name;
    if (kind === 'join' && !v('invite').trim()) st.err = 'Enter your invite code.';
    else if (!/^[a-z0-9_]{3,20}$/.test(name)) st.err = 'Fighter names are 3 to 20 letters, numbers or _.';
    else if (kind === 'join' && oathProblem(oath)) st.err = oathProblem(oath);
    else if (kind === 'join' && v('oath') !== v('oath2')) st.err = 'The passphrases don’t match.';
    else if (kind === 'join' && !c('ok')) st.err = 'Tick the box to confirm you understand it can’t be reset.';
    else if (!oath.trim()) st.err = 'Enter your passphrase.';
    if (st.err) { render(); return; }
    const keep = c('keep');
    st.busy = kind === 'join' ? 'Creating your account…' : 'Signing in…';
    render();
    try {
      if (kind === 'join') await join(name, oath, keep, v('invite'));
      else await enter(name, oath, keep);
      st.busy = '';
      stampOverlay(kind === 'join' ? 'Welcome' : 'Welcome back');
      await enterApp();
    } catch (err) {
      st.busy = '';
      st.err = err.message;
      render();
    }
    return;
  }
  if (kind === 'custom') {
    const name = v('cname').trim().replace(/\s+/g, ' ').slice(0, 40);
    if (name.length < 2) { st.err = 'Give it a name.'; render(); return; }
    const ex = { id: 'c-' + Math.random().toString(36).slice(2, 10), name, group: v('cgroup'), bw: c('cbw') };
    try {
      await addCustom(ex);
      st.picker.custom = false;
      st.picker.sel.push(ex.id);
      render();
    } catch (err) {
      st.err = err.message;
      render();
    }
    return;
  }
  if (kind === 'delete') {
    st.busy = 'Deleting…';
    render();
    try {
      await destroy(v('oath'));
      st.busy = '';
      st.draft = null;
      st.authTab = 'join';
      go('auth');
    } catch (err) {
      st.busy = '';
      st.err = err.message;
      render();
    }
  }
});

function syncChip() {
  const s = session.sync || {};
  if (s.state === 'syncing') return '<span class="sync-chip">Syncing…</span>';
  if (s.pending) return `<span class="sync-chip wait">${s.state === 'offline' ? 'Offline' : 'Waiting'} · ${s.pending}</span>`;
  if (s.state === 'offline') return '<span class="sync-chip wait">Offline</span>';
  if (s.state === 'error') return '<span class="sync-chip wait">Not synced</span>';
  return '<span class="sync-chip ok">Synced</span>';
}

onSync(() => {
  if (['home', 'history', 'progress', 'exercise'].includes(st.view)) render();
  else if (st.view === 'episode' && st.episode) {
    const el = app.querySelector('.sync-note');
    if (el) el.outerHTML = syncNote(st.episode);
    const big = app.querySelector('.ep-big');
    const entry = st.episode.id && sum().recent.find((r) => r.id === st.episode.id);
    if (big && entry) big.textContent = entry.n;
  } else {
    const el = app.querySelector('.sync-chip');
    if (el) el.outerHTML = syncChip();
  }
});

window.addEventListener('online', () => {
  syncNow();
  retryDraft((status) => { st.saveStatus = status; const el = app.querySelector('.savestate'); if (el) el.textContent = { saving: 'Saving…', saved: 'Saved', local: 'Saved on this phone. Will retry.' }[status] || ''; });
});
window.addEventListener('offline', () => { if (session.key) syncNow(); });
document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible' && session.key) syncNow(); });
setInterval(() => { if (document.visibilityState === 'visible' && session.key) syncNow(); }, 60000);

if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(() => {});

fetch('version.json', { cache: 'no-store' })
  .then((r) => (r.ok ? r.json() : null))
  .then((v) => { if (v && v.v) st.version = `${String(v.v).slice(0, 7)} · ${niceDate(String(v.at).slice(0, 10))}`; })
  .catch(() => {});

(async () => {
  render();
  const r = await restore();
  if (r.state === 'none') {
    st.lastName = r.name || '';
    st.authTab = r.name ? 'return' : 'join';
    go('auth');
    return;
  }
  await enterApp();
})();
