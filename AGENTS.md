# Training Arc

A gym tracker where your rival is you. Built for the owner first, open to anyone who signs up.
Hosted on Cloudflare (Worker + D1). Everything a user logs is encrypted on their device.

This file is also `CLAUDE.md` (a link to it), so every assistant reads the same rules.
Edit `AGENTS.md`; never replace the link with a copy.

## Read this first, every session

1. This file, top to bottom. **Latest** says where we are.
2. [docs/PRODUCT.md](docs/PRODUCT.md): what the app is and why.
3. [IDEAS.md](IDEAS.md): the idea register. Nothing gets built unless its entry says **Agreed**
   with a date.

## About the owner

- Yash (goes by Batman). Data scientist.
- **Why he is building this** (owner, 24 Oct 2026): to understand the product lifecycle, design
  language, and how to work with AI harnesses like Claude. Show the process: offer options, say
  why a choice was made, keep the decision trail in these files.
- **Fully vibe coded** (owner, 24 Oct 2026): make the technical calls yourself, explain changes in
  terms of what changed in the app, not the code.
- **Keep code comments minimal** (owner, 25 Oct 2026).
- Never use the " —" dash style in anything written for the owner (replies, docs, app copy).

## Design language

- **Bold graphic** (owner picked, 25 Oct 2026): cream paper `#F1E6D0`, ink `#141414`, red
  `#D2402C`, ghost blue `#2558C2`. Archivo Black for display (uppercase), Inter for text. Square
  corners, 2px ink borders, hard offset shadows, a big red sun as the signature shape, stamped
  results ("Beat +1", "Tied", "Ghost +2", "Boss defeated").
- **You are red, your ghost is dashed blue.** Everywhere.
- **Words are plain and to the point.** No poetic or philosophical lines (owner, 24 Oct 2026).
- **Not wanted:** ink-brush style, dark glowing "system" HUD, hand-drawn characters that look
  goofy, characters acting out each exercise (doesn't scale; owner, 25 Oct 2026).
- **Easter eggs are wanted** later (owner, 24 Oct 2026).

## How it works

- **Login is a plain passphrase** (owner: the oath sentence felt "super goofy", 25 Oct 2026).
  Sign up with a fighter name and a passphrase (10+ characters). It is normalised (lowercase,
  single spaces) and stretched on the device with PBKDF2-SHA256, 600k rounds, random salt. That
  gives two halves: a key that wraps a random AES-256 master key, and an auth key the server stores
  only as a SHA-256 hash. The server never sees the passphrase or the master key. (Code still
  calls it `oath` internally; that's fine.)
- **Invite code to join** (owner: "like vishal i want a special code needed so just no one can
  login easily", 25 Oct 2026). Stored as the Worker secret `INVITE_CODE` (set by `setup.sh`,
  changed with `npx wrangler secret put INVITE_CODE`). Checked on sign up only, case-insensitive,
  inside the sign-up rate limit (5 tries an hour per IP). No code set means sign ups are closed.
  Local dev reads it from `.dev.vars`.
- **Every record is AES-GCM encrypted on the device** with the master key, with `userId:docId` as
  associated data so records can't be swapped. The server stores only ciphertext.
- **Stay signed in on this phone** (on by default) keeps the master key in IndexedDB as a
  non-extractable key. Sessions last 180 days and renew every time the app opens, so people stay
  signed in (owner: "keep it simple, passphrase is good and then they stay signed in",
  25 Oct 2026). Lock forgets the key. A forgotten passphrase can't be reset; the app says so at sign up.
- Server: sessions are random tokens in `__Host-` cookies (Secure, HttpOnly, SameSite=Strict),
  stored hashed. Mutating requests must be JSON and same-origin. Rate limits on sign up, login and
  pre-login; 5 wrong oaths lock a name for 15 minutes; unknown names get a fake salt so names
  can't be probed. Records save with compare-and-swap (`rev`) so two devices never silently
  overwrite each other. Security headers and a strict CSP are in `public/_headers` (no inline
  scripts or styles; fonts are self-hosted).
- **Records:** `summary` (episode count, each exercise's last sets, bests, history, boss fights,
  recent episodes, custom exercises), `ep-000001`... (one per episode), `draft` (the workout in
  progress, also kept encrypted on the phone so a reload or crash loses nothing).
- **Ghost:** set N races set N from the last time you did that exercise. Bodyweight compares reps;
  weighted compares estimated 1-rep max (Epley), so a heavier set with fewer reps can still win.
- **Boss:** appears on an exercise when your best was set before your last session and your last
  session's top set was within 5% of it, at most once a week per exercise. Target: one more rep
  than your best. Win and that becomes the new best.
- **Episode titles** come from what happened: boss down, new best, boss to be continued, ghost
  beaten/won/even, or first session.

## Where things live

- `src/worker.js`: the server (API + serving `public/`).
- `migrations/`: the D1 database schema.
- `public/index.html`, `public/style.css`: the page and the whole look.
- `public/js/app.js`: screens and actions. `logic.js`: ghost, boss, episode rules.
  `store.js`: saving and loading (encrypt, compare-and-swap, drafts). `crypto.js`: the oath and
  encryption. `exercises.js`: the exercise library. `keystore.js`: IndexedDB. `api.js`: fetch.
- `checks/e2e.mjs`: the full browser check (see README).
- `.github/workflows/`: `checks.yml` (browser check on every push and PR), `deploy.yml` (push to
  `main`: checks, then database migrations and deploy; skipped until the Cloudflare secrets
  exist), `backup.yml` (daily D1 export as a 60-day artifact; owner asked for daily, 26 Oct 2026). `.github/dependabot.yml`: weekly
  dependency updates.
- `setup.sh`: one-command manual setup and deploy from the owner's Mac.
- `public/version.json`: written at deploy time (not committed); Settings shows it.
- `_archive/first-build-3d/`: the first 3D character build, kept for reference, not served.

## How we work

- **Ideas live in [IDEAS.md](IDEAS.md).**
- **Mockups before building** anything visual and new; the owner picks.
- **Owner's words as house rules**, recorded as `(owner: "his words", date)`.
- **GitHub is the source of truth:** github.com/yash161101/training-arc. Work on a branch and open
  a PR for anything non-trivial; merging to `main` deploys (owner, 25 Oct 2026: "can you maintain
  a github for this"). Never commit secrets: the invite code and Cloudflare token live in
  Cloudflare and GitHub secrets.
- **Run the browser check** before merging; GitHub runs it on every push. It must pass.
- **Deploy only when the owner says so** (merging to `main` is deploying).
- **One idea per commit.**

## Latest (start here)

**26 October 2026: auto-deploy is live.** The owner added the Cloudflare secrets (token needed
Workers Scripts: Edit added). A manual run of Deploy passed checks and deployed. From now on,
every push to `main` that passes the checks goes live. If a deploy fails, the Wrangler error
shows as an annotation on the run.

**25 October 2026: on GitHub.** Repo created by the owner; the project was pushed with a clean
history, plus CI (checks on every push), auto-deploy on `main`, weekly backups, Dependabot, and a
version line in Settings. Auto-deploy waits for the owner to add `CLOUDFLARE_API_TOKEN` and
`CLOUDFLARE_ACCOUNT_ID` as repo secrets (he will do it himself; never handle the token). First
GitHub run: checks 27/27 passed, deploy skipped as designed. The owner's Mac folder
`~/Documents/fitness_tracker` is now a clone of the repo (gh CLI signed in); after pushing, tell
him to `git pull`. Brainstormed invite codes; the owner hadn't picked one
yet.

**25 October 2026: invite code added.** Joining now needs the invite code (see How it works).
Checks 27/27. The owner runs `bash setup.sh` to deploy it; the first run asks him to choose the
code.

**25 October 2026, deployed.** The owner ran `setup.sh` and the app is live on his
workers.dev address. Then the oath wording was replaced with a plain "Passphrase" (10+
characters, Show/Hide, "Start training" / "Sign in", "Welcome back" stamp). Existing accounts
keep working (same key derivation). Checks 26/26. Redeploy with `bash setup.sh`.

**25 October 2026, later:** the owner looked at other login ideas (tag in, Face ID, generated
codes, a fighting-game combo, build your fighter, draw an emblem) and chose to keep the oath
passphrase, with people staying signed in. Sessions now last 180 days and renew on every open.

**25 October 2026: version 1 is built and passes its checks. Not deployed yet.**
After many rounds of world and character mockups that didn't land, the owner chose to build the
core first (owner: "lets build the gym app, a tracker with a simple but fun and unique login
method, recording and logging everything for users, hosted on cloudflare, secure, encrypted",
25 Oct 2026). Picked: bold graphic look; ghost on every set, episodes, boss fights, history and
progress; workouts are "pick, then repeat".

What exists: The Oath login (join, return, lock, wrong-oath lockout), home with next episode,
boss banner, repeat buttons and last episode; exercise picker (55 exercises + your own); the
workout screen (ghost on every set, reps stepper, weight carried to later sets, stamps, live
score, timer, boss fight box, add or remove sets and exercises, honest save status); episode card;
history; progress charts; settings (lock, download my data, delete account).

Checked locally with wrangler dev and headless Chromium at 390x844: `checks/e2e.mjs` 26/26.
The database was inspected: only ciphertext, no exercise names. Bad origin 403, form posts 415,
no session 401, five wrong oaths lock the name.

Next: the owner deploys (README), uses it at the gym for a week or two, then we decide what the
world/character layer should be, based on real use. Not built yet: offline-first sync (the app
needs a connection to finish an episode; drafts survive offline), changing your oath, sharing
episode cards, easter eggs.
