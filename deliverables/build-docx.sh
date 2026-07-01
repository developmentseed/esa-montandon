#!/usr/bin/env bash
# Render the ESA Montandon MTR deliverables (D1.1, D2.1, D2.2) from their
# Markdown drafts into Development-Seed house-style .docx files, then convert each
# to PDF (LibreOffice, if available). Mirrors the proposal / CNES D2 workflow.
#
# Usage:
#   ./build-docx.sh                       # build all deliverables
#   ./build-docx.sh D1.1-stac-integration # build one deliverable
#
# House style lives in assets/docx-builder/ (A4, embedded Open Sans, brand orange
# #cf3f02 on headings + table headers, DS logo cover, running header, page
# footer). Markdown's own heading levels drive the auto section numbering.
# Output lands in <deliverable>/build/ (gitignored).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
BUILDER="$HERE/assets/docx-builder"

DELIVERABLES=("D1.1-stac-integration" "D2.1-event-correlation" "D2.2-analysis-pipeline")
if [ "$#" -ge 1 ]; then
  DELIVERABLES=("$@")
fi

# Install the builder's deps once (node_modules is gitignored).
if [ ! -d "$BUILDER/node_modules" ]; then
  echo "installing docx-builder dependencies..." >&2
  (cd "$BUILDER" && npm install --silent)
fi

# Refresh Mermaid diagrams to PNG (best-effort; the builder cannot render .mmd,
# so chapters reference the committed PNGs — skip silently if rendering fails).
if [ -z "${SKIP_DIAGRAMS:-}" ]; then
  bash "$HERE/tools/render-diagrams.sh" || \
    echo "note: diagram render skipped; using committed PNGs" >&2
fi

# Locate a LibreOffice binary for the optional PDF companion.
SOFFICE="$(command -v soffice || command -v libreoffice || true)"

for d in "${DELIVERABLES[@]}"; do
  echo "=== building $d ===" >&2
  node "$BUILDER/build.mjs" "$d"
  docx="$HERE/$d/build/$d.docx"
  if [ -n "$SOFFICE" ] && [ -f "$docx" ]; then
    "$SOFFICE" --headless --convert-to pdf --outdir "$HERE/$d/build" "$docx" >/dev/null 2>&1 \
      && echo "wrote $HERE/$d/build/$d.pdf" >&2 \
      || echo "note: PDF conversion skipped for $d" >&2
  elif [ -z "$SOFFICE" ]; then
    echo "note: no LibreOffice found; skipping PDF for $d" >&2
  fi
done
