#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

say() { printf "\n\033[1;31m▶ %s\033[0m\n" "$1"; }

if ! command -v node >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then
    say "Installing Node.js with Homebrew"
    brew install node
  elif command -v conda >/dev/null 2>&1; then
    say "Installing Node.js with conda"
    conda install -y -c conda-forge "nodejs>=22"
  else
    echo "Node.js isn't installed. Get the LTS version from https://nodejs.org, then run this again."
    exit 1
  fi
fi

major=$(node -p 'process.versions.node.split(".")[0]')
if [ "$major" -lt 20 ]; then
  echo "Your Node.js is version $major. Training Arc needs 20 or newer: update it from https://nodejs.org"
  exit 1
fi

say "Installing project tools"
npm install --no-fund --no-audit

say "Signing in to Cloudflare. A browser window opens: click Allow."
if ! npx wrangler whoami 2>/dev/null | grep -qi "logged in"; then
  npx wrangler login
fi

if grep -q REPLACE_WITH_YOUR_DATABASE_ID wrangler.jsonc; then
  say "Creating the database"
  id=$(npx wrangler d1 list --json 2>/dev/null | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{try{const d=JSON.parse(s).find(x=>x.name==="training-arc");if(d)console.log(d.uuid)}catch{}})' || true)
  if [ -z "$id" ]; then
    out=$(npx wrangler d1 create training-arc </dev/null 2>&1) || { echo "$out"; exit 1; }
    id=$(printf "%s" "$out" | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' | head -1 || true)
  fi
  if [ -z "$id" ]; then
    echo "Couldn't read the database id. Run: npx wrangler d1 list"
    exit 1
  fi
  sed -i '' "s/REPLACE_WITH_YOUR_DATABASE_ID/$id/" wrangler.jsonc
  echo "Database ready: $id"
fi

say "Setting up the database tables"
npx wrangler d1 migrations apply training-arc --remote

say "Deploying Training Arc"
sha=$(git rev-parse HEAD 2>/dev/null || echo manual)
printf '{"v":"%s","at":"%s"}\n' "$sha" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > public/version.json
npx wrangler deploy

if ! npx wrangler secret list 2>/dev/null | grep -q '"INVITE_CODE"'; then
  say "Choose an invite code. Anyone who wants to join needs it."
  while true; do
    read -r -p "Invite code (at least 6 characters): " code </dev/tty
    [ ${#code} -ge 6 ] && break
    echo "Too short, try again."
  done
  printf "%s" "$code" | npx wrangler secret put INVITE_CODE
  echo "Invite code set. To change it later: npx wrangler secret put INVITE_CODE"
fi

say "Done. Open the workers.dev address above on your phone, then Share > Add to Home Screen."
