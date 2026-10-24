#!/usr/bin/env bash
# Rebuild every mock of the example, export PNGs and run the checks.
# Usage (from the repository root): bash examples/hitokoto/make.sh
set -euo pipefail
cd "$(dirname "$0")/../.."
M=examples/hitokoto/mocks
python3 examples/hitokoto/build.py
for m in light dark; do
  if [ "$m" = light ]; then bg="#F2F2F7"; else bg="#1C1C1E"; fi
  python3 scripts/frame.py pair "$M/iphone-S-01-$m.svg" "$M/iphone-S-02-$m.svg" \
    -o "$M/pair-S-01-S-02-$m.svg" --bg "$bg" \
    --caption-left "毎日ひとことだけ" --caption-right "あとから読み返せる"
  for s in outer inner; do
    python3 scripts/frame.py "duo-$s" "$M/iphone-duo-$s-S-01-$m.svg" -o "$M/framed-iphone-duo-$s-S-01-$m.svg"
  done
done
python3 scripts/export_png.py "$M"/[!f]*.svg
python3 scripts/export_png.py "$M"/framed-*.svg --bg "#F2F2F7"
python3 scripts/check_mocks.py "$M"
