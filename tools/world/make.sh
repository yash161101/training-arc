#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
out=../../public/world
mkdir -p "$out"
python3 build.py "$out"
python3 climb.py "$out" >/dev/null
python3 dojo.py "$out"
ls -la "$out"
