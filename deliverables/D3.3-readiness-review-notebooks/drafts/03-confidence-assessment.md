# Confidence Assessment

**A note on how this is weighted.** WP3's deliverables are due through December 2026. At this
checkpoint, whether the Django platform is built today is a secondary signal; the primary ones are
whether the design is sound, whether its core mechanism is validated, and whether the sequencing to
December is realistic. Ratings below reflect that.

| Deliverable | Build status | Confidence in reaching demonstrable state | Basis |
| --- | --- | --- | --- |
| D3.3 — Notebook-publishing architecture | Proposal complete; core pattern validated by WP2; Django implementation not started | **Medium-high** | Every proposed component is proven elsewhere in the stack, and its central mechanism (parameterised notebook to static output) is already running in production for WP2's Use Case 1; four open design questions need resolving (Section 4) |
| D3.1 — Training material | Not started; October start planned | **Medium-low** | Sensibly sequenced after D3.3 and the National Society consultations; ample runway to December once its inputs exist |
| D3.2 — Technical documentation (ESA JupyterLab) | Not started | **Medium-low** | Directly gated on D3.3 reaching a stable-enough state to document; documentation itself is low-risk once there is something to document |
| D3.4 — IFRC user demonstration | Not started | **Low-medium** | Last in the dependency chain; depends on all three of the above, but has runway to December |

## Basis for this pattern of confidence

WP3's confidence profile follows its dependency chain. The notebook-publishing platform (D3.3) is the
deliverable with the most engineering substance to assess: a real architecture, with proven components
and, now, a working proof of concept for its core mechanism. The other three are, at this point,
downstream commitments rather than in-progress work, which reflects a work package that only fully
starts once WP2's use cases (assessed in D2.3) exist to build on, not a team falling behind schedule.

Confidence is highest that the notebook-publishing architecture is the right design and can be built
without major rework: it reuses infrastructure this project has already proven, and its riskiest
assumption, that a parameterised notebook can be run and published without manual intervention, is
already demonstrated in production. Confidence is lowest for D3.4 landing in a fully realised,
IFRC-validated form by the Readiness Review meeting specifically, since three other deliverables need to
land first, though the December deadline gives it room to land well.

## What would raise confidence

- **D3.3** to high: the four open questions in Section 4 resolved, and a minimal, working Django +
  Celery + papermill skeleton stood up against one existing WP2 notebook.
- **D3.1** to medium: the National Society consultations (D2.3, Section 4.5) concluding on schedule,
  and at least one stable WP2 use-case notebook to train against.
- **D3.2** to medium: D3.3 reaching a state where its notebook/environment contract is fixed enough to
  document without near-term rework.
- **D3.4** to medium: a concrete demonstration date set, once D3.1–D3.3 are far enough along to support
  one.

## Framing

WP3 is not behind schedule relative to its planned sequencing: MapAction's own stated plan was always to
start training material in October, after consultations and first-version tools. Measured against "is
this demonstrable today," the answer for three of WP3's four deliverables is no, and that is expected
this far ahead of the December deadline. The Readiness Review meeting is the right venue to confirm that
this sequencing remains the agreed plan.
