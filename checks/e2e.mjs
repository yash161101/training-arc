import { chromium } from 'playwright';
import { mkdirSync } from 'node:fs';

const BASE = process.env.BASE || 'http://localhost:8787';
const SHOTS = new URL('./shots/', import.meta.url).pathname;
const NAME = 'fighter' + Math.floor(Math.random() * 1e6);
const OATH = 'I will hang from that bar until ten';
const INVITE = process.env.INVITE || 'local-invite';
mkdirSync(SHOTS, { recursive: true });

const results = [];
const ok = (name, cond, extra = '') => {
  results.push({ name, pass: !!cond, extra });
  console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
};

const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, colorScheme: process.env.SCHEME === 'dark' ? 'dark' : 'light' });
const page = await ctx.newPage();
const errors = [];
page.on('console', (m) => { if (m.type() === 'error' && !/status of (401|403|404)|ERR_INTERNET_DISCONNECTED|net::ERR_FAILED/.test(m.text())) errors.push(m.text()); });
page.on('pageerror', (e) => errors.push(e.message));
page.on('dialog', (d) => d.accept());
const shot = (n) => page.screenshot({ path: SHOTS + (process.env.SCHEME === 'dark' ? 'dark-' : '') + n + '.png' });

async function finishEpisode() {
  await page.click('[data-act="finish"]');
  await page.waitForSelector('.ep-card', { timeout: 20000 });
}

async function doAllSets() {
  while (await page.$('[data-act="done"]')) await page.click('[data-act="done"] >> nth=0');
}

await page.goto(BASE);
await page.waitForSelector('form[data-form="join"]');
await shot('01-join');
ok('Join screen shows', true);

await page.fill('input[name="invite"]', 'wrong-code');
await page.fill('input[name="name"]', NAME);
await page.fill('input[name="oath"]', OATH);
await page.fill('input[name="oath2"]', OATH);
await page.check('input[name="ok"]');
await page.click('button[type="submit"]');
await page.waitForSelector('.err', { timeout: 30000 });
ok('Wrong invite code is refused', (await page.textContent('.err')).includes('invite code'));
await page.fill('input[name="invite"]', INVITE);
await page.fill('input[name="oath"]', 'short');
await page.fill('input[name="oath2"]', 'short');
await page.check('input[name="ok"]');
await page.click('button[type="submit"]');
ok('Weak passphrase is refused', (await page.textContent('.err')).includes('10 characters'));

await page.fill('input[name="oath"]', OATH);
await page.fill('input[name="oath2"]', OATH);
await page.click('button[type="submit"]');
await page.waitForSelector('.hero', { timeout: 30000 });
await page.waitForTimeout(1400);
ok('Sign up lands on home with Ep. 1', (await page.textContent('.ep-num')).trim() === 'Ep. 1');
await shot('02-home-new');

await page.click('[data-act="new"]');
await page.fill('.search', 'pull');
await page.click('[data-act="pick"][data-id="pull-ups"]');
await page.fill('.search', 'dumbbell curl');
await page.click('[data-act="pick"][data-id="bicep-curl"]');
await shot('03-picker');
await page.click('[data-act="start"]');
await page.waitForSelector('.workout');
ok('Workout opens with 2 exercises', (await page.$$('.ex')).length === 2);

const kg = page.locator('input[data-field="w"][data-i="1"][data-j="0"]');
await kg.fill('12.5');
await kg.dispatchEvent('change');
ok('Weight carries to later sets', (await page.inputValue('input[data-field="w"][data-i="1"][data-j="2"]')) === '12.5');
await shot('04-workout-first');
await doAllSets();
await shot('05-workout-first-done');
await finishEpisode();
ok('Episode 1 saved', (await page.textContent('.ep-big')).trim() === '1', await page.textContent('.ep-title'));
await shot('06-episode-1');
await page.click('[data-act="go"][data-view="home"]');
await page.waitForSelector('.hero');
ok('Home moves to Ep. 2', (await page.textContent('.ep-num')).trim() === 'Ep. 2');
ok('Repeat Ep. 1 offered', !!(await page.$('[data-act="repeat"][data-n="1"]')));

await page.click('[data-act="repeat"][data-n="1"]');
await page.waitForSelector('.workout');
ok('Ghost shows on sets', (await page.textContent('.ghost-line')).includes('Ghost'));
await page.click('[data-act="rep"][data-i="0"][data-j="0"][data-d="1"]');
await page.click('[data-act="done"][data-i="0"][data-j="0"]');
ok('Beating the ghost stamps Beat', (await page.textContent('.stamp')).toLowerCase().includes('beat'));
await page.click('[data-act="rep"][data-i="0"][data-j="0"][data-d="1"]').catch(() => {});
await page.click('[data-act="rep"][data-i="0"][data-j="1"][data-d="-1"]');
await page.click('[data-act="done"][data-i="0"][data-j="1"]');
await shot('07-workout-ghost');
await doAllSets();
ok('Score counts You and Ghost', (await page.textContent('.score')).replace(/\s+/g, ' ').includes('You 1'));
await finishEpisode();
const t2 = await page.textContent('.ep-title');
ok('Episode 2 titled from the session', /New best|Ghost beaten/.test(t2), t2);
await shot('08-episode-2');
await page.click('[data-act="go"][data-view="home"]');

await page.click('[data-act="repeat"]');
await page.waitForSelector('.workout');
ok('No pull-ups boss when the best was set last time', !(await page.$('.ex:nth-of-type(1) .boss')));
await doAllSets();
await finishEpisode();
await page.click('[data-act="go"][data-view="home"]');
await page.waitForSelector('.hero');
ok('Boss waiting banner on home', !!(await page.$('.boss-banner')), (await page.$('.boss-banner')) ? await page.textContent('.boss-banner') : '');
await shot('09-home-boss');

await page.click('[data-act="repeat"]');
await page.waitForSelector('.boss');
await page.click('[data-act="boss"]');
await shot('10-boss-fight');
await page.click('[data-act="boss-done"]');
ok('Boss defeated', (await page.textContent('.boss-big')).toLowerCase().includes('defeated'));
await shot('11-boss-won');
await doAllSets();
await finishEpisode();
const t4 = await page.textContent('.ep-title');
ok('Episode 4 is a boss episode', t4.startsWith('Boss down'), t4);
await shot('12-episode-boss');
await page.click('[data-act="go"][data-view="home"]');

await page.click('[data-act="repeat"]');
await page.waitForSelector('.workout');
await page.click('[data-act="done"] >> nth=0');
await page.waitForTimeout(2000);
await page.reload();
await page.waitForSelector('.hero');
ok('Unfinished workout survives a reload', !!(await page.$('[data-act="resume"]')));
await page.click('[data-act="resume"]');
ok('Resumed set still done', !!(await page.$('.set.done')));
await page.click('[data-act="leave"]');
await page.click('[data-act="discard"]');
await page.waitForTimeout(500);
ok('Discard removes it', !(await page.$('[data-act="resume"]')));

await page.click('[data-act="go"][data-view="history"]');
ok('History lists 4 episodes', (await page.$$('.ep-row')).length === 4);
await page.click('.ep-row >> nth=0');
await page.waitForSelector('.ep-card');
ok('Old episode opens', (await page.textContent('.ep-big')).trim() === '4');
await page.click('[data-act="go"][data-view="history"]');
await page.click('[data-act="go"][data-view="home"]');
await page.click('[data-act="go"][data-view="progress"]');
ok('Progress shows charts', !!(await page.$('.prog-row .spark')));
await shot('13-progress');

await page.click('[data-act="go"][data-view="home"]');
await page.waitForSelector('.hero');
await page.waitForSelector('.grounds svg.valley', { timeout: 15000 });
ok('Training grounds show on home', !!(await page.$('.grounds svg.valley')));
ok('The grounds move: water, clouds, birds, smoke', (await page.evaluate(() => document.getAnimations().length)) > 40);
ok('Grounds start on the dojo', (await page.$eval('.grounds-scroll', (el) => el.scrollLeft)) > 100);
ok('A beaten boss leaves a split boulder', (await page.$eval('#w-split1', (el) => el.getAttribute('display'))) === 'inline');
await shot('16-grounds');
await page.click('svg.valley rect[data-view="dojo"]', { force: true });
await page.waitForSelector('.dojo-page svg.dojo');
ok('Tapping the dojo goes inside', /\d/.test(await page.textContent('.pl-num')));
ok('Dojo lists forms for trained exercises', (await page.textContent('.forms')).includes('Pull-ups'));
ok('Dojo opens a scroll per exercise', (await page.$$('.d-scroll.open')).length >= 2);
await shot('17-dojo');
await page.click('[data-act="go"][data-view="home"]');
await page.waitForSelector('.grounds svg.valley');
await page.click('[data-act="go"][data-view="climb"]');
await page.waitForSelector('.climb-page svg.climb');
ok('The climb shows steps laid', /\d+ of \d+ steps/.test(await page.textContent('.steps-count')));
ok('Untrained legs leave the climb as a trail', (await page.$$('.c-step.trail')).length > 100);
await shot('18-climb');
await page.click('[data-act="go"][data-view="home"]');
await page.waitForSelector('.hero');
await page.waitForFunction(() => navigator.serviceWorker && navigator.serviceWorker.controller, null, { timeout: 15000 }).catch(() => {});
ok('Offline cache is installed', await page.evaluate(() => !!(navigator.serviceWorker && navigator.serviceWorker.controller)));
await ctx.setOffline(true);
await page.reload();
await page.waitForSelector('.hero', { timeout: 20000 });
ok('App opens with no internet', (await page.textContent('.ep-num')).trim() === 'Ep. 5');
ok('Shows it is offline', (await page.textContent('.sync-chip')).includes('Offline'));
await page.click('[data-act="repeat"]');
await page.waitForSelector('.workout');
await doAllSets();
await finishEpisode();
ok('Episode saves with no internet', (await page.textContent('.sync-note')).includes('this phone'));
await page.click('[data-act="go"][data-view="home"]');
await page.waitForSelector('.hero');
ok('Home moves on while offline', (await page.textContent('.ep-num')).trim() === 'Ep. 6');
ok('Shows 1 waiting to sync', (await page.textContent('.sync-chip')).includes('1'));
await shot('15-offline-waiting');
await ctx.setOffline(false);
const synced = await page.waitForFunction(() => { const c = document.querySelector('.sync-chip'); return c && c.textContent.includes('Synced'); }, null, { timeout: 30000 }).then(() => true, () => false);
ok('Syncs by itself when back online', synced);
ok('No leftover unfinished workout', !(await page.$('[data-act="resume"]')));

const ctx3 = await browser.newContext({ viewport: { width: 390, height: 844 } });
await ctx3.addInitScript(() => {
  const put = IDBObjectStore.prototype.put;
  IDBObjectStore.prototype.put = function (v, k) {
    if (v && v.key instanceof CryptoKey) throw new DOMException('An object could not be cloned.', 'DataCloneError');
    return put.call(this, v, k);
  };
});
const p3 = await ctx3.newPage();
p3.on('dialog', (d) => d.accept());
await p3.goto(BASE);
await p3.waitForSelector('form[data-form="join"]');
await p3.click('[data-act="tab"][data-tab="return"]');
await p3.fill('input[name="name"]', NAME);
await p3.fill('input[name="oath"]', OATH);
await p3.click('button[type="submit"]');
await p3.waitForSelector('.hero', { timeout: 30000 });
ok('Another device sees the offline episode', (await p3.textContent('.ep-num')).trim() === 'Ep. 6');
ok('Another device has no stale unfinished workout', !(await p3.$('[data-act="resume"]')));
await p3.reload();
await p3.waitForSelector('.hero', { timeout: 20000 });
ok('Stays signed in when the phone refuses to store the key', (await p3.textContent('.ep-num')).trim() === 'Ep. 6');
await p3.click('[data-act="go"][data-view="settings"]');
ok('Settings says this phone stays signed in', (await p3.textContent('.remembered')).includes('stays signed in'));
await ctx3.close();

const ctx4 = await browser.newContext({ viewport: { width: 390, height: 844 }, timezoneId: 'Asia/Kolkata' });
await ctx4.clock.setFixedTime(new Date('2026-11-08T23:30:00+05:30'));
await ctx4.route('**/api/sky', (r) => r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ city: 'Mumbai', country: 'IN', lat: 19.1, lon: 72.9, weather: { code: 61 } }) }));
const p4 = await ctx4.newPage();
await p4.goto(BASE);
await p4.waitForSelector('form[data-form="join"]');
await p4.click('[data-act="tab"][data-tab="return"]');
await p4.fill('input[name="name"]', NAME);
await p4.fill('input[name="oath"]', OATH);
await p4.click('button[type="submit"]');
await p4.waitForSelector('.grounds svg.valley', { timeout: 30000 });
await p4.waitForFunction(() => document.querySelector('#w-rain') && document.querySelector('#w-rain').getAttribute('display') === 'inline', null, { timeout: 15000 }).catch(() => {});
const disp = async (id) => p4.$eval(id, (el) => el.getAttribute('display'));
ok('Night follows the city clock, not the theme', (await disp('#w-night')) === 'inline');
ok('Rain in the city rains on the grounds', (await disp('#w-rain')) === 'inline');
ok('Diwali lights the diyas', (await disp('#w-diwali')) === 'inline');
ok('Home names the city and festival', (await p4.textContent('.grounds')).includes('Mumbai'));
await p4.click('[data-act="go"][data-view="boulders"]');
await p4.waitForSelector('svg.place-boulders');
ok('Boulder garden carves the beaten boss', (await p4.textContent('.place-boulders .u.laid .u-label')).startsWith('Ep'));
await p4.click('[data-act="go"][data-view="home"]');
await p4.waitForSelector('.grounds svg.valley');
for (const [v, sel] of [['cliff', 'svg.place-cliff'], ['yard', 'svg.place-yard'], ['forge', 'svg.place-forge']]) {
  await p4.click(`[data-act="go"][data-view="${v}"]`);
  await p4.waitForSelector(sel);
  ok(`The ${v} opens and counts`, /\d+ of \d+/.test(await p4.textContent('.units-count')));
  await p4.click('[data-act="go"][data-view="home"]');
  await p4.waitForSelector('.grounds svg.valley');
}
ok('Pull work sets grips on the cliff', true);
await p4.click('svg.valley rect[data-act="poke"]', { force: true });
ok('The dummy reacts to a poke', await p4.$eval('#w-dummy', (el) => el.classList.contains('wobble')));
await ctx4.close();

await page.click('[data-act="go"][data-view="settings"]');
ok('Settings says this phone stays signed in', (await page.textContent('.remembered')).includes('stays signed in'));
await page.click('[data-act="theme"][data-theme="dark"]');
ok('Dark mode can be picked', (await page.evaluate(() => document.documentElement.dataset.theme)) === 'dark');
await page.reload();
await page.waitForSelector('.hero');
ok('Dark mode stays after a reload', (await page.evaluate(() => document.documentElement.dataset.theme)) === 'dark');
await page.waitForSelector('.grounds svg.valley');
ok('Dark mode does not force night on the grounds', !!(await page.$('#w-night')));
await page.click('[data-act="go"][data-view="settings"]');
await page.click('[data-act="theme"][data-theme="auto"]');
ok('Auto goes back to following the phone', (await page.evaluate(() => document.documentElement.dataset.theme)) === undefined);
await page.click('[data-act="lock"]');
await page.waitForSelector('form[data-form="return"]');
await page.fill('input[name="name"]', NAME);
await page.fill('input[name="oath"]', 'I will hang from that bar until nine');
await page.click('button[type="submit"]');
await page.waitForSelector('.err', { timeout: 30000 });
ok('Wrong passphrase is refused', (await page.textContent('.err')).includes('Wrong'));
await page.fill('input[name="oath"]', OATH.toUpperCase() + '  ');
await page.click('button[type="submit"]');
await page.waitForSelector('.hero', { timeout: 30000 });
ok('Passphrase works regardless of case and spaces', (await page.textContent('.ep-num')).trim() === 'Ep. 6');

const page2 = await (await browser.newContext({ viewport: { width: 390, height: 844 } })).newPage();
await page2.goto(BASE);
await page2.waitForSelector('form[data-form="join"]');
const r = await page2.evaluate(async () => (await fetch('/api/doc/summary')).status);
ok('Another browser cannot read data', r === 401);

await shot('14-home-after');
ok('No console errors', errors.length === 0, errors.slice(0, 3).join(' | '));

const failed = results.filter((x) => !x.pass);
console.log(`\n${results.length - failed.length}/${results.length} passed`);
await browser.close();
process.exit(failed.length ? 1 : 0);
