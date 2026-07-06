#!/usr/bin/env bash
# Render every Mermaid diagram (deliverables/*/figures/*.mmd) to PNG.
#
# The .mmd sources are the editable single source of truth (they also render
# inline on GitHub / in the IDE). The Markdown -> docx builder cannot render
# Mermaid, so the chapters reference the pre-rendered PNGs. Commit both.
#
# Usage: ./tools/render-diagrams.sh
# Requires Node (npx); pulls @mermaid-js/mermaid-cli on first run. Uses a system
# Chrome/Chromium when found (via a puppeteer config), otherwise lets
# mermaid-cli download its own.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
DELIV="$(cd "$HERE/.." && pwd)"

shopt -s nullglob
sources=("$DELIV"/*/figures/*.mmd)
if [ ${#sources[@]} -eq 0 ]; then
  echo "no *.mmd sources under $DELIV/*/figures" >&2
  exit 0
fi

# Point puppeteer at a system Chrome when available (avoids a large download).
PCFG=""
for b in google-chrome google-chrome-stable chromium chromium-browser; do
  if command -v "$b" >/dev/null 2>&1; then
    PCFG="$(mktemp)"
    printf '{"executablePath":"%s","args":["--no-sandbox"]}' "$(command -v "$b")" >"$PCFG"
    echo "using Chrome: $(command -v "$b")" >&2
    break
  fi
done

rendered=0
for src in "${sources[@]}"; do
  out="${src%.mmd}.png"
  echo "rendering $(basename "$(dirname "$(dirname "$src")")")/$(basename "$src")" >&2
  args=(-i "$src" -o "$out" -b white -s 2)
  [ -n "$PCFG" ] && args+=(-p "$PCFG")
  npx -y @mermaid-js/mermaid-cli "${args[@]}"
  rendered=$((rendered + 1))
done

echo "done: $rendered diagram(s) rendered" >&2
