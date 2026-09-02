# Introduction and Scope

## Purpose of this report

This document is deliverable **D3.3 — Readiness Review Report of the Analytics Services Notebooks**,
produced under Work Package 3 of the ESA activity "Application Development concerning Disaster Data and
Analytics" (SoW ESA-EOP-SG-OF-0779). It gives ESA, IFRC, MapAction, and Development Seed a shared,
candid picture of readiness across WP3 ahead of the Readiness Review meeting.

## Why this report covers all of WP3, not only the notebook-publishing platform

WP3 comprises four deliverables, all children of the same work package:

- **D3.1** — Training material for relevant user communities.
- **D3.2** — Technical documentation for integration into ESA JupyterLab environments.
- **D3.3** — This report, and the notebook-publishing platform it primarily assesses.
- **D3.4** — Report of the demonstration of the analytics services with IFRC users.

The notebook-publishing platform (D3.3's namesake) is WP3's central piece of engineering — it is what
D3.1 trains users on, what D3.2 documents for ESA JupyterLab integration, and what D3.4 demonstrates.
Because the four are this tightly coupled, we assess readiness across all four here rather than treating
D3.3 as an isolated engineering artefact. This scope was confirmed with the deliverable owner ahead of
drafting.

## What "the notebook-publishing platform" means

The core proposal — detailed in Section 2 — is a Django application that lets a defined set of users:

- select an **analysis notebook template** (an exposure, impact, or prioritisation notebook from WP2)
  and the parameters it takes (administrative area, hazard, data source, and so on);
- **trigger a run**, which executes the notebook against those parameters as a background job and
  publishes the result as a static, shareable output;
- **browse and discover** previously generated analyses by country, administrative area, or event; and,
  for select authorised users,
- **author new notebooks from a template**, rather than only running existing ones.

This is deliberately built on the same modular-notebook model established by WP2's automated analysis
pipeline (deliverable D2.2) — the notebooks this platform runs are the same artefacts, or close
relatives of them, that WP2's event-driven pipeline runs automatically. WP3 adds the human-driven,
on-demand counterpart to WP2's event-driven automation.

## Relationship to other deliverables

This platform is downstream of WP1 (the data model, D1.1) and WP2 (the notebooks and pipeline
architecture, D2.1/D2.2, and the use cases assessed for readiness in D2.3). It is upstream of D3.1
(training on it), D3.2 (documenting it for ESA), and D3.4 (demonstrating it to IFRC users). Deliverable
D2.4 (case studies) is also formally nested under WP3 in the project's issue tracker, though numbered
D2.x; we note this only for completeness and do not duplicate its coverage here, since it is assessed on
its own terms in D2.3.

## Scope of this assessment

This report covers: the state of work for each of the four WP3 deliverables (Section 2); a consolidated
confidence assessment (Section 3); open questions and blockers (Section 4); the implementation plan
(Section 5); and conclusions and next steps (Section 6). It does not re-litigate the WP2 pipeline
architecture or use-case status, which are assessed in D2.2 and D2.3 respectively, though it depends on
both.
