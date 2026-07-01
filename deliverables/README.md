# ESA Montandon — MTR Deliverables

Mid-Term Review (MTR) technical-assessment reports for the ESA activity *Application Development
concerning Disaster Data and Analytics* (RFP ESA RFP/3-19182/26/I-DT-bgh, SoW ESA-EOP-SG-OF-0779).

| Ref | Report | WP |
| --- | --- | --- |
| **D1.1** | STAC Integration and Interoperability | WP1 |
| **D2.1** | Event Correlation System adapted to relevant EO Data Products | WP2 |
| **D2.2** | Automated Analysis Pipeline combining Structured Disaster Data with EO Hazard Layers | WP2 |

Each report opens with an executive summary written for the ESA Technical Officer (strategic /
organisational framing), followed by the technical body.

## Layout

```
deliverables/
  assets/docx-builder/     # Node `docx` house-style renderer (reused from the CNES D2 report)
  build-docx.sh            # builds all deliverables (or one, by name) to .docx (+ PDF if LibreOffice)
  <deliverable>/
    metadata.yaml          # cover front-matter (deliverable ref, RFP/SoW, version, date, authors)
    drafts/NN-*.md         # ordered Markdown chapters (concatenated in filename order)
    figures/               # figure PNGs (optional; diagrams are currently inline ASCII/tables)
    build/                 # generated .docx (gitignored)
```

## Build

```bash
cd deliverables
./build-docx.sh                        # build all three
./build-docx.sh D1.1-stac-integration  # build one
```

The script installs the builder's npm dependencies on first run and writes
`<deliverable>/build/<deliverable>.docx`. It also attempts a PDF via LibreOffice (`soffice`) when
available; the `.docx` is the primary artifact.

## Editing

- Content lives in `<deliverable>/drafts/*.md`. Headings are **auto-numbered** by the renderer — write
  `#`, `##`, `###` without manual numbers.
- Markdown tables, fenced code blocks, blockquotes, and images (from `figures/`) are supported.
- House style (fonts, brand colour, cover, header/footer) is in `assets/docx-builder/lib/`. To place an
  ESA logo on the cover, drop a PNG into `assets/docx-builder/img/` and expose it as `img.esa` in
  `lib/theme.mjs` (the cover slot is already wired).

## Sources

Content is grounded in the released Monty STAC extension **v1.3.0** (`IFRCGo/monty-stac-extension`) —
the Response taxonomy, best-practices, correlation, and Response↔Impact boundary docs — plus the WP1
issue history in `developmentseed/esa-montandon` and the project proposal.
