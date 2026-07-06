// Cover page, running header and footer for the D2 report.

import zlib from "node:zlib";
import {
  Paragraph,
  TextRun,
  ImageRun,
  Table,
  TableRow,
  TableCell,
  WidthType,
  BorderStyle,
  AlignmentType,
  Header,
  Footer,
  PageNumber,
  PageBreak,
  VerticalAlign,
  HorizontalPositionRelativeFrom,
  VerticalPositionRelativeFrom,
  InternalHyperlink,
} from "docx";
import { COLOR, FONT, SIZE, img } from "./theme.mjs";

const EMU_PER_IN = 914400;

// Rounded-rectangle PNG (RGBA, 1px anti-aliased) so the brand accent bar has
// soft pill ends. Rendered at 2x for smoother corners; no binary asset needed.
function roundedBarPng(hex, w, h, radius) {
  const r = parseInt(hex.slice(0, 2), 16);
  const g = parseInt(hex.slice(2, 4), 16);
  const b = parseInt(hex.slice(4, 6), 16);
  const coverage = (x, y) => {
    // distance outside the rounded region; 1 inside, 0 outside, AA between
    let cx = null;
    let cy = null;
    if (x < radius) cx = radius;
    else if (x > w - 1 - radius) cx = w - 1 - radius;
    if (y < radius) cy = radius;
    else if (y > h - 1 - radius) cy = h - 1 - radius;
    if (cx === null || cy === null) return 1;
    const d = Math.hypot(x - cx, y - cy);
    return Math.max(0, Math.min(1, radius - d + 0.5));
  };
  const raw = Buffer.alloc((w * 4 + 1) * h);
  for (let y = 0; y < h; y += 1) {
    let o = y * (w * 4 + 1);
    raw[o++] = 0; // filter: none
    for (let x = 0; x < w; x += 1) {
      raw[o++] = r;
      raw[o++] = g;
      raw[o++] = b;
      raw[o++] = Math.round(255 * coverage(x, y));
    }
  }
  const chunk = (type, data) => {
    const len = Buffer.alloc(4);
    len.writeUInt32BE(data.length, 0);
    const body = Buffer.concat([Buffer.from(type, "ascii"), data]);
    const crc = Buffer.alloc(4);
    crc.writeUInt32BE(zlib.crc32(body) >>> 0, 0);
    return Buffer.concat([len, body, crc]);
  };
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(w, 0);
  ihdr.writeUInt32BE(h, 4);
  ihdr[8] = 8; // bit depth
  ihdr[9] = 6; // colour type: truecolour + alpha
  return Buffer.concat([
    Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]),
    chunk("IHDR", ihdr),
    chunk("IDAT", zlib.deflateSync(raw)),
    chunk("IEND", Buffer.alloc(0)),
  ]);
}

// 2x source (36 x 860, r=18) scaled down on display for crisp pill ends.
const accentBarData = roundedBarPng(COLOR.brand, 80, 860, 10);

const NO_BORDERS = {
  top: { style: BorderStyle.NONE, size: 0, color: "auto" },
  bottom: { style: BorderStyle.NONE, size: 0, color: "auto" },
  left: { style: BorderStyle.NONE, size: 0, color: "auto" },
  right: { style: BorderStyle.NONE, size: 0, color: "auto" },
  insideHorizontal: { style: BorderStyle.NONE, size: 0, color: "auto" },
  insideVertical: { style: BorderStyle.NONE, size: 0, color: "auto" },
};

// A thick brand horizontal rule, used as the cover accent.
function brandRule(spaceBefore = 240, spaceAfter = 240) {
  return new Paragraph({
    spacing: { before: spaceBefore, after: spaceAfter },
    border: { bottom: { style: BorderStyle.SINGLE, size: 24, color: COLOR.brand, space: 1 } },
  });
}

export function buildCover(meta) {
  const children = [];

  // logo (ds-logo.png is 750 x 128) + the floating brand accent bar that
  // bleeds off the bottom-left of the cover.
  children.push(
    new Paragraph({
      spacing: { before: 240, after: 480 },
      children: [
        new ImageRun({
          type: "png",
          data: img.cover,
          transformation: { width: 250, height: 43 },
        }),
        new ImageRun({
          type: "png",
          data: accentBarData,
          transformation: { width: 18, height: 430 },
          floating: {
            horizontalPosition: {
              relative: HorizontalPositionRelativeFrom.PAGE,
              offset: Math.round(1.5 * EMU_PER_IN),
            },
            verticalPosition: {
              relative: VerticalPositionRelativeFrom.PAGE,
              offset: Math.round(8.1 * EMU_PER_IN),
            },
            allowOverlap: true,
            behindDocument: true,
          },
        }),
        // Partner/client logo slot (top-right of the cover) — populated only
        // when an ESA logo asset is dropped into img/ and exposed as img.esa in
        // theme.mjs. Omitted otherwise; ESA/MapAction are carried textually in
        // the FOR/BY cover metadata below, with the DS logo top-left.
        ...(img.esa
          ? [
              new ImageRun({
                type: "png",
                data: img.esa,
                // ESA wordmark is 2.5:1; keep aspect ratio (140 x 56 px).
                transformation: { width: 140, height: 56 },
                floating: {
                  horizontalPosition: {
                    // right edge flush to the ~0.79in (2cm) page margin
                    relative: HorizontalPositionRelativeFrom.PAGE,
                    offset: Math.round((8.27 - 0.79 - 140 / 96) * EMU_PER_IN),
                  },
                  verticalPosition: {
                    relative: VerticalPositionRelativeFrom.PAGE,
                    offset: Math.round(0.8 * EMU_PER_IN),
                  },
                  allowOverlap: true,
                  behindDocument: false,
                },
              }),
            ]
          : []),
      ],
    }),
  );

  // title
  children.push(
    new Paragraph({
      spacing: { before: 1200, after: 80 },
      children: [
        new TextRun({ text: meta.title, bold: true, size: SIZE.title, color: COLOR.title }),
      ],
    }),
  );

  // subtitle
  if (meta.subtitle) {
    children.push(
      new Paragraph({
        spacing: { after: 200 },
        children: [
          new TextRun({ text: meta.subtitle, size: SIZE.subtitle, color: COLOR.muted }),
        ],
      }),
    );
  }

  children.push(brandRule(120, 1000));

  // metadata table (DELIVERABLE / FOR / BY / SUBJECT / REFERENCE / … / DATE)
  const rows = [
    ["DELIVERABLE", meta.deliverable],
    ["FOR", meta.for],
    ["BY", meta.by],
    ["SUBJECT", meta.title],
    ["REFERENCE", meta.reference],
    ["RFP", meta.rfp],
    ["SOW", meta.sow],
    ["VERSION", meta.version],
    ["DATE", meta.date],
  ].filter(([, v]) => v);

  children.push(
    new Table({
      width: { size: 100, type: WidthType.PERCENTAGE },
      borders: NO_BORDERS,
      columnWidths: [1800, 7000],
      rows: rows.map(
        ([label, value]) =>
          new TableRow({
            children: [
              new TableCell({
                width: { size: 1800, type: WidthType.DXA },
                margins: { top: 40, bottom: 40, left: 0, right: 120 },
                children: [
                  new Paragraph({
                    spacing: { after: 0, line: 276 },
                    children: [
                      new TextRun({ text: label, size: SIZE.small, color: COLOR.muted }),
                    ],
                  }),
                ],
              }),
              new TableCell({
                width: { size: 7000, type: WidthType.DXA },
                margins: { top: 40, bottom: 40, left: 0, right: 0 },
                children: [
                  new Paragraph({
                    spacing: { after: 0, line: 276 },
                    children: [
                      new TextRun({ text: String(value), size: SIZE.body, color: COLOR.body }),
                    ],
                  }),
                ],
              }),
            ],
          }),
      ),
    }),
  );

  // push the body to a fresh page
  children.push(new Paragraph({ children: [new PageBreak()] }));
  return children;
}

// Static, always-populated Contents (clickable internal links, no page numbers
// so it needs no field update). Chapters + sections only (levels 1-2).
export function buildToc(headings) {
  const out = [
    new Paragraph({
      spacing: { before: 0, after: 200 },
      children: [new TextRun({ text: "Contents", size: SIZE.h1, color: COLOR.brand })],
    }),
  ];
  for (const h of headings.filter((x) => x.level <= 2)) {
    out.push(
      new Paragraph({
        spacing: { before: h.level === 1 ? 100 : 10, after: 10, line: 264 },
        indent: { left: (h.level - 1) * 360 },
        children: [
          new InternalHyperlink({
            anchor: h.anchor,
            children: [
              new TextRun({
                text: h.text,
                size: SIZE.body,
                color: h.level === 1 ? COLOR.title : COLOR.body,
              }),
            ],
          }),
        ],
      }),
    );
  }
  return out;
}

export function buildHeader(meta) {
  return new Header({
    children: [
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        borders: NO_BORDERS,
        columnWidths: [6000, 3000],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                verticalAlign: VerticalAlign.CENTER,
                margins: { top: 0, bottom: 0, left: 0, right: 0 },
                children: [
                  new Paragraph({
                    spacing: { after: 0 },
                    children: [
                      new TextRun({
                        text: meta.runningTitle || meta.title,
                        size: SIZE.small,
                        color: COLOR.muted,
                      }),
                    ],
                  }),
                ],
              }),
              new TableCell({
                verticalAlign: VerticalAlign.CENTER,
                margins: { top: 0, bottom: 0, left: 0, right: 0 },
                children: [
                  new Paragraph({
                    alignment: AlignmentType.RIGHT,
                    spacing: { after: 0 },
                    children: [
                      new ImageRun({
                        type: "png",
                        data: img.header,
                        transformation: { width: 118, height: 23 },
                      }),
                    ],
                  }),
                ],
              }),
            ],
          }),
        ],
      }),
      // spacer so the body starts well below the running header
      new Paragraph({ spacing: { before: 0, after: 0, line: 360, lineRule: "auto" }, children: [] }),
    ],
  });
}

export function buildFooter() {
  return new Footer({
    children: [
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        spacing: { before: 0, after: 0 },
        children: [
          new TextRun({ text: "Page ", size: SIZE.small, color: COLOR.muted }),
          new TextRun({ children: [PageNumber.CURRENT], size: SIZE.small, color: COLOR.muted }),
        ],
      }),
    ],
  });
}
