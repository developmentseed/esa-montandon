# Introduction and Scope

## Purpose of this report

This document is deliverable **D2.3 — Readiness Review Report**, produced under Work Package 2 of the
ESA activity "Application Development concerning Disaster Data and Analytics" (SoW ESA-EOP-SG-OF-0779).
It is due ahead of the Readiness Review meeting and is intended to give ESA, IFRC, MapAction, and
Development Seed a shared, candid picture of where WP2 execution stands: what is built, what is
confident to land on schedule, what is not, and why.

This is explicitly a **status and planning document**, not a technical design document. The
architecture it reports against — the event-driven pipeline, the modular-notebook model, and the
data-combination pattern — was assessed and fixed in deliverable **D2.2** (July 2026) and is not
revisited here except where execution has surfaced a gap in that design.

## Relationship to the other WP2 deliverables

WP2's deliverable chain builds progressively:

- **D2.1** (delivered) specified the event-correlation system that ties EO products to the correct
  disaster record.
- **D2.2** (delivered) specified the automated analysis pipeline that combines structured data with EO
  hazard layers, using that correlation system as its matching engine.
- **D2.3** (this report) assesses readiness: how far execution has progressed against the D2.2
  architecture, for each of the three use cases it is designed to serve.
- **D2.4** (forthcoming) will document the finished case studies — the three use cases fully realised,
  demonstrated against real events, with reusability guidance for other application contexts. A first
  narrative draft of the three use cases, prepared for ESA in July 2026 ahead of this report, already
  exists in this repository and is referenced throughout as the definition of what each use case is
  meant to deliver.

## What "readiness" means here

For each use case, this report assesses readiness along three dimensions:

1. **Build status** — what notebooks, applications, and data pipelines exist today, evidenced by merged
   or open pull requests and by the state of the underlying data.
2. **Validation status** — whether the use case has been run against a real or realistic event, and
   whether it has been reviewed by IFRC or MapAction domain experts.
3. **Path to demonstrable** — what remains before the use case could be shown to an IFRC user as a
   working example, and our confidence in reaching that state on the WP2 execution timeline.

## Scope of this assessment

This report covers: the state of work for each of the three use cases (Section 2); a consolidated
confidence assessment (Section 3); open questions and blockers, including two risks that affect all
three use cases regardless of individual progress (Section 4); the implementation plan to close
remaining gaps (Section 5); and conclusions and next steps (Section 6).

It does not re-assess the underlying data model (D1.1), the correlation system (D2.1), or the pipeline
architecture (D2.2) — all three are treated as a settled foundation. It also does not attempt to
pre-empt D2.4: where a use case's methodology is already fully specified (as with Use Case 3), this
report assesses build progress against that specification rather than re-deriving it.
