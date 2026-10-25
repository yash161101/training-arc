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
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
const page = await ctx.newPage();
const errors = [];
page.on('console', (m) => { if (m.type() === 'error' && !/status of (401|403|404)/.test(m.text())) errors.push(m.text()); });
page.on('pageerror', (e) => errors.push(e.message));
page.on('dialog', (d) => d.accept());
const shot = (n) => page.screenshot({ path: SHOTS + n + '.png' });

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
await page.click('[data-act="go"][data-view="settings"]');
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
ok('Passphrase works regardless of case and spaces', (await page.textContent('.ep-num')).trim() === 'Ep. 5');

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
