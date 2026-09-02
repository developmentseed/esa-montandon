# Confidence Assessment

| Deliverable | Build status | Confidence in reaching demonstrable state | Basis |
| --- | --- | --- | --- |
| D3.3 — Notebook-publishing architecture | Proposal complete; no implementation | **Medium** | Every proposed component is proven elsewhere in the stack; four open design questions need resolving first (Section 4) |
| D3.1 — Training material | Not started; October start planned | **Low-medium** | Sensibly sequenced after D3.3 and the National Society consultations, but that means real content does not exist yet |
| D3.2 — Technical documentation (ESA JupyterLab) | Not started | **Low-medium** | Directly gated on D3.3 reaching a stable-enough state to document; documentation itself is low-risk once there is something to document |
| D3.4 — IFRC user demonstration | Not started | **Low** | Last in the dependency chain; depends on all three of the above |

## Why this pattern of confidence

WP3's confidence profile is a straight reflection of its dependency chain: the notebook-publishing
platform (D3.3) is the one deliverable with engineering substance to assess — a real architecture, with
proven components and a small number of genuinely open design questions — while the other three are, at
this point, downstream commitments rather than in-progress work. This is not a sign of the team being
behind; it is the honest state of a work package that only fully starts once WP2's use cases (assessed
in D2.3) exist to build on.

We are **most confident** that the notebook-publishing architecture is the right design and can be built
without major rework, because it reuses infrastructure this project has already proven (Django-adjacent
patterns are new, but Celery, Kubernetes, papermill, and object storage are not). We are **least
confident** in D3.4 landing in a fully realised, IFRC-validated form by the Readiness Review meeting,
simply because three other things need to happen first.

## What would raise our confidence

- **D3.3** → medium to medium-high: the four open questions in Section 4 resolved, and a minimal,
  working Django + Celery + papermill skeleton stood up against one existing WP2 notebook.
- **D3.1** → low-medium to medium: the National Society consultations (D2.3, Section 4.4) concluding on
  schedule, and at least one stable WP2 use-case notebook to train against.
- **D3.2** → low-medium to medium: D3.3 reaching a state where its notebook/environment contract is
  fixed enough to document without near-term rework.
- **D3.4** → low to low-medium: a concrete demonstration date set, once D3.1–D3.3 are far enough along
  to support one.

## What we are not claiming

We are not claiming WP3 is behind schedule relative to its planned sequencing — MapAction's own stated
plan was always to start training material in October, after consultations and first-version tools. We
are claiming that, measured against "is this demonstrable today," the honest answer for three of WP3's
four deliverables is no, and that the Readiness Review meeting is the right venue to confirm that this
sequencing is still the agreed plan rather than assume it.
