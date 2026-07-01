// Markdown -> docx block elements, in the DS house style.
// Uses markdown-it tokens. Lists are rendered with explicit bullet / number
// runs (no numbering.xml machinery) so they restart correctly and render the
// same in every viewer.

import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import {
  Paragraph,
  TextRun,
  ExternalHyperlink,
  ImageRun,
  Table,
  TableRow,
  TableCell,
  WidthType,
  BorderStyle,
  HeadingLevel,
  ShadingType,
  VerticalAlign,
  Bookmark,
} from "docx";
import { COLOR, FONT, SIZE } from "./theme.mjs";

const HEADING_LEVEL = {
  1: HeadingLevel.HEADING_1,
  2: HeadingLevel.HEADING_2,
  3: HeadingLevel.HEADING_3,
  4: HeadingLevel.HEADING_4,
  5: HeadingLevel.HEADING_4,
  6: HeadingLevel.HEADING_4,
};
const HEADING_SIZE = { 1: SIZE.h1, 2: SIZE.h2, 3: SIZE.h3, 4: SIZE.h4, 5: SIZE.h4, 6: SIZE.h4 };

const cellBorder = { style: BorderStyle.SINGLE, size: 4, color: COLOR.rule };
const CELL_BORDERS = {
  top: cellBorder,
  bottom: cellBorder,
  left: cellBorder,
  right: cellBorder,
};

// width/height from a PNG IHDR header.
function pngSize(buf) {
  if (buf.length > 24 && buf.readUInt32BE(12) === 0x49484452) {
    return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
  }
  return { width: 600, height: 400 };
}

// width/height from a JPEG SOF marker.
function jpegSize(buf) {
  let i = 2;
  while (i < buf.length - 1) {
    if (buf[i] !== 0xff) {
      i += 1;
      continue;
    }
    const m = buf[i + 1];
    // SOF markers carry the frame dimensions
    if ((m >= 0xc0 && m <= 0xc3) || (m >= 0xc5 && m <= 0xc7) || (m >= 0xc9 && m <= 0xcb) || (m >= 0xcd && m <= 0xcf)) {
      return { height: buf.readUInt16BE(i + 5), width: buf.readUInt16BE(i + 7) };
    }
    if (m === 0xd8 || m === 0xd9 || (m >= 0xd0 && m <= 0xd7)) {
      i += 2;
      continue;
    }
    i += 2 + buf.readUInt16BE(i + 2);
  }
  return { width: 600, height: 400 };
}

// image type ("png" | "jpg") and pixel size, from the file extension + bytes.
function imageInfo(src, buf) {
  const ext = path.extname(src).toLowerCase();
  if (ext === ".jpg" || ext === ".jpeg") {
    return { type: "jpg", ...jpegSize(buf) };
  }
  return { type: "png", ...pngSize(buf) };
}

// Figures display at <= 600px wide, so embedding multi-thousand-pixel source
// images just bloats the .docx. Cap the embedded copy's longest edge via
// ImageMagick, cached beside the source (originals untouched). Degrades to the
// original bytes if ImageMagick is unavailable or conversion fails.
const MAX_EMBED_PX = 1600;
let convertOK = null;
function hasConvert() {
  if (convertOK === null) {
    try {
      execFileSync("convert", ["-version"], { stdio: "ignore" });
      convertOK = true;
    } catch {
      convertOK = false;
    }
  }
  return convertOK;
}
function cacheConvert(file, ext, extraArgs) {
  const dir = path.join(path.dirname(file), ".cache");
  fs.mkdirSync(dir, { recursive: true });
  const mtime = Math.floor(fs.statSync(file).mtimeMs);
  const out = path.join(dir, `${path.basename(file)}.${MAX_EMBED_PX}.${mtime}${ext}`);
  if (!fs.existsSync(out)) {
    execFileSync("convert", [file, "-resize", `${MAX_EMBED_PX}x${MAX_EMBED_PX}>`, "-strip", ...extraArgs, out], {
      stdio: "ignore",
    });
  }
  return fs.readFileSync(out);
}

// Prepare an image for embedding: returns { type, data, width, height } or null.
// WebP (which Word cannot embed) is converted to PNG; over-large PNG/JPEG are
// downscaled. Falls back to the original bytes if ImageMagick is unavailable.
function prepareEmbed(file) {
  const ext = path.extname(file).toLowerCase();
  const original = fs.readFileSync(file);
  if (ext === ".webp") {
    if (!hasConvert()) return null; // cannot embed webp without conversion
    try {
      const data = cacheConvert(file, ".png", []);
      return { type: "png", data, ...pngSize(data) };
    } catch {
      return null;
    }
  }
  const info = imageInfo(file, original); // { type, width, height }
  if (Math.max(info.width, info.height) <= MAX_EMBED_PX || !hasConvert()) {
    return { type: info.type, data: original, width: info.width, height: info.height };
  }
  try {
    const data = cacheConvert(file, ext, ["-quality", "82"]);
    return { type: info.type, data, width: info.width, height: info.height };
  } catch {
    return { type: info.type, data: original, width: info.width, height: info.height };
  }
}

export function createRenderer({ figuresBase }) {
  const headings = []; // collected for the static table of contents
  let bmCounter = 0;
  // ---- inline ----
  // opts: { forceColor, forceBold } — used for table-header (white bold) cells.
  function renderInline(tokens, inherited = {}, opts = {}) {
    const runs = [];
    const stack = { bold: false, italics: false, strike: false, ...inherited };
    let linkHref = null;
    let linkRuns = null;

    const pushText = (text, extra = {}) => {
      const run = new TextRun({
        text,
        font: FONT.sans,
        size: opts.forceSize || SIZE.body,
        color: opts.forceColor || (linkHref ? COLOR.brand : COLOR.body),
        bold: opts.forceBold || stack.bold,
        italics: opts.forceItalics || stack.italics,
        strike: stack.strike,
        underline: linkHref && !opts.forceColor ? {} : undefined,
        ...extra,
      });
      (linkRuns || runs).push(run);
    };

    for (const t of tokens) {
      switch (t.type) {
        case "text":
          if (t.content) pushText(t.content);
          break;
        case "softbreak":
          pushText(" ");
          break;
        case "hardbreak":
          (linkRuns || runs).push(new TextRun({ break: 1 }));
          break;
        case "strong_open":
          stack.bold = true;
          break;
        case "strong_close":
          stack.bold = false;
          break;
        case "em_open":
          stack.italics = true;
          break;
        case "em_close":
          stack.italics = false;
          break;
        case "s_open":
          stack.strike = true;
          break;
        case "s_close":
          stack.strike = false;
          break;
        case "code_inline":
          (linkRuns || runs).push(
            new TextRun({
              text: t.content,
              font: FONT.mono,
              size: SIZE.body - 1,
              color: COLOR.body,
              shading: { type: ShadingType.CLEAR, fill: COLOR.zebra, color: "auto" },
            }),
          );
          break;
        case "link_open":
          linkHref = t.attrGet("href");
          linkRuns = [];
          break;
        case "link_close":
          runs.push(new ExternalHyperlink({ link: linkHref, children: linkRuns }));
          linkHref = null;
          linkRuns = null;
          break;
        case "image":
          // handled at block level; ignore inline image text here
          break;
        default:
          if (t.children) runs.push(...renderInline(t.children, stack));
      }
    }
    return runs;
  }

  // a paragraph that is just an image -> figure + caption
  function imageBlock(inlineToken) {
    const imgTok = inlineToken.children.find((c) => c.type === "image");
    if (!imgTok) return null;
    const src = imgTok.attrGet("src");
    const alt = imgTok.content || (imgTok.children || []).map((c) => c.content).join("");
    const file = path.resolve(figuresBase, src);
    const out = [];
    const prepared = fs.existsSync(file) ? prepareEmbed(file) : null;
    if (prepared) {
      const { type, data, width, height } = prepared;
      const maxW = 600; // page text width (px @96dpi)
      const maxH = 840; // keep tall diagrams within one A4 page
      let w = Math.min(maxW, width);
      let h = Math.round((w / width) * height);
      if (h > maxH) {
        h = maxH;
        w = Math.round((maxH / height) * width);
      }
      out.push(
        new Paragraph({
          alignment: "center",
          spacing: { before: 120, after: 80 },
          children: [new ImageRun({ type, data, transformation: { width: w, height: h } })],
        }),
      );
    }
    if (alt) {
      out.push(
        new Paragraph({
          style: "Caption",
          children: renderInline([{ type: "text", content: alt }], {}, {
            forceSize: SIZE.caption,
            forceItalics: true,
            forceColor: COLOR.muted,
          }),
        }),
      );
    }
    return out;
  }

  // ---- table ----
  function buildTable(rows) {
    const ncol = rows.length ? rows[0].cells.length : 0;
    const tableRows = rows.map((row, ri) =>
      new TableRow({
        tableHeader: row.header,
        children: row.cells.map(
          (cellTokens) =>
            new TableCell({
              verticalAlign: VerticalAlign.CENTER,
              margins: { top: 60, bottom: 60, left: 100, right: 100 },
              shading: row.header
                ? { type: ShadingType.CLEAR, fill: COLOR.brand, color: "auto" }
                : ri % 2 === 0
                  ? { type: ShadingType.CLEAR, fill: COLOR.zebra, color: "auto" }
                  : undefined,
              children: [
                new Paragraph({
                  spacing: { before: 20, after: 20, line: 264 },
                  children: row.header
                    ? renderInline(cellTokens, {}, { forceColor: COLOR.headerText, forceBold: true })
                    : renderInline(cellTokens),
                }),
              ],
            }),
        ),
      }),
    );
    return new Table({
      width: { size: 100, type: WidthType.PERCENTAGE },
      borders: {
        top: cellBorder,
        bottom: cellBorder,
        left: cellBorder,
        right: cellBorder,
        insideHorizontal: cellBorder,
        insideVertical: cellBorder,
      },
      rows: tableRows,
      columnWidths: Array(ncol).fill(Math.floor(9026 / Math.max(1, ncol))),
    });
  }

  // ---- block walk ----
  function walk(tokens) {
    const out = [];
    let i = 0;
    const counters = [0, 0, 0, 0, 0, 0];

    // Strip any author-typed leading number ("1", "1.1", "6 —", "1. ") so the
    // generated numbering is the only one, then build a consistent prefix:
    // H1 -> "1.", H2 -> "1.1", H3 -> "1.1.1".
    const headingPrefix = (level) => {
      counters[level - 1] += 1;
      for (let k = level; k < counters.length; k += 1) counters[k] = 0;
      const parts = counters.slice(0, level);
      return level === 1 ? `${parts[0]}.` : parts.join(".");
    };
    const stripLeadingNumber = (s) =>
      s.replace(/^\s*\d+(\.\d+)*\s*(—|–|-|\.|:)?\s*/, "");

    // returns [blocks, newIndex] for the content until matching close at depth
    const collectListItems = (start, ordered, depth) => {
      const blocks = [];
      let j = start;
      let counter = 0;
      while (j < tokens.length && tokens[j].type !== (ordered ? "ordered_list_close" : "bullet_list_close")) {
        if (tokens[j].type === "list_item_open") {
          counter += 1;
          const marker = ordered ? `${counter}.` : "•";
          j += 1;
          let first = true;
          while (j < tokens.length && tokens[j].type !== "list_item_close") {
            const tk = tokens[j];
            if (tk.type === "paragraph_open") {
              const inline = tokens[j + 1];
              const runs = renderInline(inline.children);
              blocks.push(
                new Paragraph({
                  spacing: { before: first ? 40 : 20, after: 40, line: 268 },
                  indent: { left: 360 + depth * 360, hanging: 240 },
                  children: [
                    new TextRun({ text: `${marker}\t`, color: COLOR.body, size: SIZE.body }),
                    ...runs,
                  ],
                }),
              );
              first = false;
              j += 3; // paragraph_open, inline, paragraph_close
            } else if (tk.type === "bullet_list_open" || tk.type === "ordered_list_open") {
              const nested = collectListItems(j + 1, tk.type === "ordered_list_open", depth + 1);
              blocks.push(...nested.blocks);
              j = nested.index + 1; // past *_list_close
            } else {
              j += 1;
            }
          }
          j += 1; // list_item_close
        } else {
          j += 1;
        }
      }
      return { blocks, index: j };
    };

    while (i < tokens.length) {
      const t = tokens[i];
      switch (t.type) {
        case "heading_open": {
          const level = Number(t.tag.slice(1));
          const inline = tokens[i + 1];
          const prefix = headingPrefix(level);
          const size = HEADING_SIZE[level];
          // strip any pre-typed number from the first text token
          const kids = (inline.children || []).map((c, idx) =>
            idx === 0 && c.type === "text"
              ? { ...c, content: stripLeadingNumber(c.content) }
              : c,
          );
          const runs = renderInline(kids, {}, {
            forceColor: COLOR.heading,
            forceSize: size,
          });
          runs.unshift(
            new TextRun({
              text: `${prefix} `,
              font: FONT.sans,
              color: COLOR.heading,
              size,
            }),
          );
          const plain =
            `${prefix} ` +
            kids.map((c) => (c.type === "text" ? c.content : c.content || "")).join("");
          const anchor = `sec_${++bmCounter}`;
          if (level <= 3) headings.push({ level, text: plain.replace(/\s+/g, " ").trim(), anchor });
          out.push(
            new Paragraph({
              heading: HEADING_LEVEL[level],
              pageBreakBefore: level === 1,
              children: [new Bookmark({ id: anchor, children: runs })],
            }),
          );
          i += 3;
          break;
        }
        case "paragraph_open": {
          const inline = tokens[i + 1];
          const hasImage = inline.children && inline.children.some((c) => c.type === "image");
          if (hasImage) {
            const blocks = imageBlock(inline);
            if (blocks) out.push(...blocks);
          } else {
            out.push(new Paragraph({ children: renderInline(inline.children) }));
          }
          i += 3;
          break;
        }
        case "blockquote_open": {
          // status notes etc. -> Status style
          let j = i + 1;
          while (j < tokens.length && tokens[j].type !== "blockquote_close") {
            if (tokens[j].type === "paragraph_open") {
              const inline = tokens[j + 1];
              out.push(new Paragraph({ style: "Status", children: renderInline(inline.children) }));
              j += 3;
            } else {
              j += 1;
            }
          }
          // borderless spacer so the gap after the quote isn't traced by the
          // brand left bar (a paragraph border spans its own spacing)
          out.push(new Paragraph({ spacing: { before: 0, after: 0, line: 200 }, children: [] }));
          i = j + 1;
          break;
        }
        case "bullet_list_open":
        case "ordered_list_open": {
          const res = collectListItems(i + 1, t.type === "ordered_list_open", 0);
          out.push(...res.blocks);
          i = res.index + 1;
          break;
        }
        case "table_open": {
          const rows = [];
          let j = i + 1;
          let inHead = false;
          while (j < tokens.length && tokens[j].type !== "table_close") {
            const tk = tokens[j];
            if (tk.type === "thead_open") inHead = true;
            else if (tk.type === "thead_close") inHead = false;
            else if (tk.type === "tr_open") {
              const cells = [];
              j += 1;
              while (tokens[j].type !== "tr_close") {
                if (tokens[j].type === "th_open" || tokens[j].type === "td_open") {
                  const inline = tokens[j + 1];
                  cells.push(inline.children || []);
                  j += 3;
                } else {
                  j += 1;
                }
              }
              rows.push({ header: inHead, cells });
            }
            j += 1;
          }
          out.push(buildTable(rows));
          out.push(new Paragraph({ spacing: { before: 0, after: 0, line: 120 }, children: [] }));
          i = j + 1;
          break;
        }
        case "fence":
        case "code_block": {
          // Monospace code block: shaded, with a brand left rule. markdown-it
          // has no dedicated docx renderer for these, so build it explicitly.
          const lines = t.content.replace(/\n+$/, "").split("\n");
          const kids = [];
          lines.forEach((line, idx) => {
            if (idx > 0) kids.push(new TextRun({ break: 1 }));
            kids.push(
              new TextRun({
                text: line.length ? line : " ",
                font: FONT.mono,
                size: SIZE.body - 2,
                color: COLOR.body,
              }),
            );
          });
          out.push(
            new Paragraph({
              spacing: { before: 80, after: 120, line: 240 },
              shading: { type: ShadingType.CLEAR, fill: COLOR.zebra, color: "auto" },
              border: { left: { style: BorderStyle.SINGLE, size: 12, color: COLOR.brand, space: 6 } },
              children: kids,
            }),
          );
          i += 1;
          break;
        }
        case "hr": {
          out.push(
            new Paragraph({
              spacing: { before: 120, after: 120 },
              border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: COLOR.rule } },
            }),
          );
          i += 1;
          break;
        }
        default:
          i += 1;
      }
    }
    return out;
  }

  return { walk, headings };
}
