# Training Arc

A gym tracker where your rival is you. Every set races your ghost from last time; your best-ever
self shows up as a boss; every session is an episode. Everything you log is encrypted on your
phone before it is saved.

Rules and decisions: [AGENTS.md](AGENTS.md). Product story: [docs/PRODUCT.md](docs/PRODUCT.md).
Ideas: [IDEAS.md](IDEAS.md).

## How changes go live

The code lives at github.com/yash161101/training-arc. Every push runs the full browser check on
GitHub. A push to `main` that passes deploys to Cloudflare automatically (database updates
included), once the two Cloudflare secrets below are set. A daily job also saves a database
backup (encrypted data only) as a downloadable file, kept for 60 days.

### Turn on auto-deploy (once)

1. In Cloudflare: **My Profile → API Tokens → Create Token → "Edit Cloudflare Workers"** template.
   Add one more permission: **Account · D1 · Edit**. Create it and copy the token.
2. In Cloudflare, copy your **Account ID** (Workers & Pages overview, right side).
3. In GitHub: **repo → Settings → Secrets and variables → Actions → New repository secret**.
   Add `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`.

Until both are set, deploys are skipped (checks still run).

### Make this folder track GitHub (once)

```
brew install gh
gh auth login
gh auth setup-git
cd ~/Documents/fitness_tracker
git init -b main
git remote add origin https://github.com/yash161101/training-arc.git
git fetch origin
git reset --hard origin/main
```

`gh auth login` signs Terminal in to GitHub (pick GitHub.com, HTTPS, log in with a browser). The
last line makes the folder match GitHub exactly; your `node_modules`, `.wrangler` and `_archive`
folders are ignored and stay put.

After that, `git pull` brings in changes made elsewhere.

## Put it online by hand (one command)

Make a free Cloudflare account first (dash.cloudflare.com/sign-up). Then in Terminal:

```
bash ~/Documents/fitness_tracker/setup.sh
```

It installs Node.js if needed, signs you in to Cloudflare (click Allow in the browser), creates
the database, sets up the tables, deploys, and the first time asks you to choose an **invite
code**. Nobody can join without it; share it only with people you want in. Change it any time
with `npx wrangler secret put INVITE_CODE` (existing accounts keep working). Run it again any time to redeploy. Stay on the free
plan: don't add a payment method or upgrade to Workers Paid.

## Put it online by hand (first time, about 5 minutes)

You need Node.js once (nodejs.org, the LTS version). Then, in Terminal, inside this folder:

```
npm install
npx wrangler login
npx wrangler d1 create training-arc
```

The last command prints a `database_id`. Paste it into `wrangler.jsonc` in place of
`REPLACE_WITH_YOUR_DATABASE_ID`. Then:

```
npm run db:remote
npm run deploy
```

`deploy` prints your app's address, like `https://training-arc.<you>.workers.dev`.

Or open this folder in Claude Code and say "set it up and deploy it".

## On your phone

Open the address in Safari, tap Share, then **Add to Home Screen**.

## Run it on your laptop

Copy `.dev.vars.example` to `.dev.vars` (it holds a local invite code), then:

```
npm run db:local
npm run dev
```

Open http://localhost:8787.

## Check it works

With `npm run dev` running in another window (the check uses the invite code from `.dev.vars`):

```
npx playwright install chromium
INVITE=pick-a-code-for-local-testing npm run check
```

It signs up a test fighter, logs four episodes, beats a ghost, fights a boss, reloads mid-workout,
locks and logs back in. Screenshots land in `checks/shots/`.
