# Confidence Assessment

| Deliverable | Build status | Confidence in reaching demonstrable state | Basis |
| --- | --- | --- | --- |
| D3.3 — Notebook-publishing architecture | Proposal complete; no implementation | **Medium** | Every proposed component is proven elsewhere in the stack; four open design questions need resolving first (Section 4) |
| D3.1 — Training material | Not started; October start planned | **Low-medium** | Sensibly sequenced after D3.3 and the National Society consultations, but no content exists yet |
| D3.2 — Technical documentation (ESA JupyterLab) | Not started | **Low-medium** | Directly gated on D3.3 reaching a stable-enough state to document; documentation itself is low-risk once there is something to document |
| D3.4 — IFRC user demonstration | Not started | **Low** | Last in the dependency chain; depends on all three of the above |

## Basis for this pattern of confidence

WP3's confidence profile follows its dependency chain directly. The notebook-publishing platform (D3.3)
is the one deliverable with engineering substance to assess: a real architecture, with proven components
and a small number of open design questions. The other three are, at this point, downstream commitments
rather than in-progress work. This reflects a work package that only fully starts once WP2's use cases
(assessed in D2.3) exist to build on, not a team falling behind.

Confidence is highest that the notebook-publishing architecture is the right design and can be built
without major rework, since it reuses infrastructure this project has already proven (Django-adjacent
patterns are new, but Celery, Kubernetes, papermill, and object storage are not). Confidence is lowest
for D3.4 landing in a fully realised, IFRC-validated form by the Readiness Review meeting, since three
other deliverables need to land first.

## What would raise confidence

- **D3.3** to medium/medium-high: the four open questions in Section 4 resolved, and a minimal, working
  Django + Celery + papermill skeleton stood up against one existing WP2 notebook.
- **D3.1** to low-medium/medium: the National Society consultations (D2.3, Section 4.4) concluding on
  schedule, and at least one stable WP2 use-case notebook to train against.
- **D3.2** to low-medium/medium: D3.3 reaching a state where its notebook/environment contract is fixed
  enough to document without near-term rework.
- **D3.4** to low/low-medium: a concrete demonstration date set, once D3.1–D3.3 are far enough along to
  support one.

## Framing

WP3 is not behind schedule relative to its planned sequencing: MapAction's own stated plan was always to
start training material in October, after consultations and first-version tools. Measured against "is
this demonstrable today," the answer for three of WP3's four deliverables is no. The Readiness Review
meeting is the right venue to confirm that this sequencing remains the agreed plan.
