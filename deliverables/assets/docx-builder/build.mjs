// Build one ESA Montandon deliverable .docx from its Markdown drafts, in the
// Development Seed house style. Generalized from the CNES D2 builder: the target
// deliverable directory is passed as the first CLI argument.
//
//   node build.mjs D1.1-stac-integration
//
// It reads <deliverable>/metadata.yaml, concatenates <deliverable>/drafts/*.md in
// filename order, resolves figures from <deliverable>/figures/, and writes
// <deliverable>/build/<deliverable>.docx.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";
import MarkdownIt from "markdown-it";
import { Document, Packer } from "docx";

import { styles, fonts, PAGE } from "./lib/theme.mjs";
import { buildCover, buildToc, buildHeader, buildFooter } from "./lib/chrome.mjs";
import { createRenderer } from "./lib/render.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DELIVERABLES = path.resolve(HERE, "..", ".."); // repo/deliverables

const target = process.argv[2];
if (!target) {
  console.error("usage: node build.mjs <deliverable-dir>  (e.g. D1.1-stac-integration)");
  process.exit(1);
}
const REPORT = path.join(DELIVERABLES, target);
const DRAFTS = path.join(REPORT, "drafts");
const FIGURES = path.join(REPORT, "figures");
if (!fs.existsSync(DRAFTS)) {
  console.error(`no drafts/ directory found under ${REPORT}`);
  process.exit(1);
}

function loadMeta() {
  const file = path.join(REPORT, "metadata.yaml");
  const raw = fs.existsSync(file) ? fs.readFileSync(file, "utf8") : "";
  const m = yaml.load(raw.replace(/^---\s*$/gm, "")) || {};
  return {
    title: m.title || target,
    subtitle: m.subtitle || "",
    date: m.date || "",
    by: m.by || "Development Seed & MapAction",
    for: m.for || "European Space Agency — ESRIN",
    version: m.version || "1.0",
    deliverable: m.deliverable || "",
    reference: m.reference || "",
    rfp: m.rfp || "",
    sow: m.sow || "",
    runningTitle: m.runningTitle || m.title || target,
  };
}

function readMarkdown() {
  const files = fs
    .readdirSync(DRAFTS)
    .filter((f) => f.toLowerCase().endsWith(".md"))
    .sort();
  if (!files.length) {
    console.error(`no .md files in ${DRAFTS}`);
    process.exit(1);
  }
  return files.map((f) => fs.readFileSync(path.join(DRAFTS, f), "utf8")).join("\n\n");
}

function main() {
  const meta = loadMeta();
  const md = new MarkdownIt({ html: false, linkify: true, typographer: false });
  const tokens = md.parse(readMarkdown(), {});

  const { walk, headings } = createRenderer({ figuresBase: FIGURES });
  const body = walk(tokens);
  const toc = buildToc(headings);

  const doc = new Document({
    creator: "Development Seed",
    title: meta.title,
    description: `${meta.deliverable} ${meta.title}`.trim(),
    styles,
    fonts,
    sections: [
      {
        properties: {
          page: { size: PAGE.size, margin: PAGE.margin },
          titlePage: true,
        },
        headers: { default: buildHeader(meta) },
        footers: { default: buildFooter() },
        children: [...buildCover(meta), ...toc, ...body],
      },
    ],
  });

  const outDir = path.join(REPORT, "build");
  fs.mkdirSync(outDir, { recursive: true });
  const out = path.join(outDir, `${target}.docx`);
  Packer.toBuffer(doc).then((buf) => {
    fs.writeFileSync(out, buf);
    console.log("wrote", out, `(${(buf.length / 1024).toFixed(0)} KiB)`);
  });
}

main();
