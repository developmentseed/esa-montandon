// Development Seed house style for the D2 strategic report.
// Single source of truth for fonts, colours, sizes and spacing. Mirrors the
// proposal template (A4, Open Sans, brand orange on headers/accents) but with a
// near-black body for crisp reading, per review feedback.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const root = (...p) => path.join(HERE, "..", ...p);

export const COLOR = {
  brand: "CF3F02", // DS secondary — table-header fill, accent bar
  heading: "534E4E", // section headings — grey, uncoloured (bold carries them)
  title: "434343", // cover title — dark grey
  body: "534E4E", // general text grey (DS house body colour)
  muted: "666666", // subtitle, captions, header chrome
  rule: "DDDDDD", // light table / divider rules
  zebra: "F7F5F4", // faint warm zebra for table body rows
  headerText: "FFFFFF", // text on the brand-filled table header
};

export const FONT = {
  sans: "Open Sans",
  mono: "DejaVu Sans Mono",
};

// half-point sizes
export const SIZE = {
  body: 20, // 10pt
  small: 18, // 9pt (header/footer)
  caption: 16, // 8pt figure captions
  title: 44, // 22pt cover title
  subtitle: 24, // 12pt cover subtitle
  h1: 40, // 20pt
  h2: 32, // 16pt
  h3: 28, // 14pt
  h4: 24, // 12pt
};

export const fonts = [
  { name: FONT.sans, data: fs.readFileSync(root("fonts/OpenSans-regular.ttf")) },
  { name: FONT.sans, data: fs.readFileSync(root("fonts/OpenSans-bold.ttf")), bold: true },
  { name: FONT.sans, data: fs.readFileSync(root("fonts/OpenSans-italic.ttf")), italic: true },
  {
    name: FONT.sans,
    data: fs.readFileSync(root("fonts/OpenSans-boldItalic.ttf")),
    bold: true,
    italic: true,
  },
];

export const img = {
  cover: fs.readFileSync(root("img/ds-logo.png")),
  header: fs.readFileSync(root("img/ds-logo-header.png")),
  esa: fs.readFileSync(root("img/esa-logo.png")), // 1378 x 551 wordmark (2.5:1)
};

// Paragraph + character styles passed to the docx Document.
export const styles = {
  default: {
    document: {
      run: { font: FONT.sans, size: SIZE.body, color: COLOR.body },
      paragraph: {
        spacing: { line: 276, lineRule: "auto", after: 160 },
      },
    },
  },
  paragraphStyles: [
    {
      id: "Heading1",
      name: "Heading 1",
      basedOn: "Normal",
      next: "Normal",
      quickFormat: true,
      run: { size: SIZE.h1, bold: false, color: COLOR.heading },
      paragraph: { spacing: { before: 320, after: 100 }, keepNext: true },
    },
    {
      id: "Heading2",
      name: "Heading 2",
      basedOn: "Normal",
      next: "Normal",
      quickFormat: true,
      run: { size: SIZE.h2, bold: false, color: COLOR.heading },
      paragraph: { spacing: { before: 240, after: 80 }, keepNext: true },
    },
    {
      id: "Heading3",
      name: "Heading 3",
      basedOn: "Normal",
      next: "Normal",
      quickFormat: true,
      run: { size: SIZE.h3, bold: false, color: COLOR.heading },
      paragraph: { spacing: { before: 200, after: 60 }, keepNext: true },
    },
    {
      id: "Heading4",
      name: "Heading 4",
      basedOn: "Normal",
      next: "Normal",
      quickFormat: true,
      run: { size: SIZE.h4, bold: false, color: COLOR.heading },
      paragraph: { spacing: { before: 160, after: 60 }, keepNext: true },
    },
    {
      id: "Caption",
      name: "Caption",
      basedOn: "Normal",
      next: "Normal",
      run: { size: SIZE.caption, italics: true, color: COLOR.muted },
      paragraph: { spacing: { before: 40, after: 240 }, alignment: "center" },
    },
    {
      id: "Status",
      name: "Status note",
      basedOn: "Normal",
      next: "Normal",
      run: { size: SIZE.small, color: COLOR.muted },
      paragraph: {
        spacing: { before: 60, after: 40 },
        indent: { left: 360 },
        border: { left: { style: "single", size: 18, space: 12, color: COLOR.brand } },
      },
    },
  ],
};

// A4 section geometry, matching the proposal template (twips).
export const PAGE = {
  size: { width: 11906, height: 16838, orientation: "portrait" },
  margin: { top: 1152, bottom: 1152, left: 1440, right: 1440, header: 720, footer: 720 },
};
