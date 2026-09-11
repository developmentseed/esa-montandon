# Confidence Assessment

**A note on how this is weighted.** WP3's deliverables are due through December 2026. At this
checkpoint, whether a specific implementation is built today is a secondary signal; the primary ones are
whether the pipeline's core pieces are sound, whether they are individually validated, and whether the
sequencing to December is realistic. Ratings below reflect that.

| Deliverable | Build status | Confidence in reaching demonstrable state | Basis |
| --- | --- | --- | --- |
| D3.3 — Notebook-publishing pipeline | Four core pieces identified; 2 of 4 already running in production via WP2 | **Medium-high** | Notebook generation and static-site compilation are proven; triggering and distribution are not yet designed (see per-piece breakdown below); four open design questions need resolving (Section 4) |
| D3.1 — Training material | Not started; October start planned | **Medium-low** | Sensibly sequenced after D3.3 and the National Society consultations; ample runway to December once its inputs exist |
| D3.2 — Technical documentation (ESA JupyterLab) | Not started | **Medium-low** | Directly gated on D3.3 reaching a stable-enough state to document; documentation itself is low-risk once there is something to document |
| D3.4 — IFRC user demonstration | Not started | **Low-medium** | Last in the dependency chain; depends on all three of the above, but has runway to December |

## D3.3 core: confidence by pipeline piece

Rather than rate the notebook-publishing pipeline as a single architecture, confidence is assessed per
functional piece (Section 2.1), since the four pieces carry very different amounts of risk:

| Piece | Status | Confidence | Basis |
| --- | --- | --- | --- |
| Triggers | Automated-event trigger proven, reused from WP2; manual and scheduled triggering not built | **Medium** | The proven path is reused infrastructure; the unbuilt path needs a backing service and a light UI, neither of which exists yet |
| Notebook generation | Running in production for WP2 Use Case 1 | **High** | Parameterised, papermill-executed notebooks already run end to end, validated for more than one country |
| Static site compilation | Running in production for WP2 Use Case 1's single path | **High** | The MyST build to static HTML already works; generalising it to arbitrary on-demand runs is an extension, not new design |
| Access and distribution | A live URL exists for the one published site; email notification and external-platform integration (for example, GO) are undesigned | **Low-medium** | The hosting half is proven; the notification and integration half has no specification yet |

## Basis for this pattern of confidence

WP3's confidence profile follows its dependency chain. The notebook-publishing platform (D3.3) is the
deliverable with the most engineering substance to assess: a real architecture, with proven components
and, now, a working proof of concept for its core mechanism. The other three are, at this point,
downstream commitments rather than in-progress work, which reflects a work package that only fully
starts once WP2's use cases (assessed in D2.3) exist to build on, not a team falling behind schedule.

Confidence is highest for the two pipeline pieces already proven in production, notebook generation and
static-site compilation: the platform's riskiest assumption, that a parameterised notebook can be run and
published without manual intervention, is already demonstrated. Confidence is lower for the
still-undesigned trigger and distribution pieces, though neither carries architectural risk, only undone
design and build work. Confidence is lowest for D3.4 landing in a fully realised,
IFRC-validated form by the Readiness Review meeting specifically, since three other deliverables need to
land first, though the December deadline gives it room to land well.

## What would raise confidence

- **D3.3** to high: the four open questions in Section 4 resolved, and a minimal, working trigger stood
  up end to end, one manual or scheduled run through all four pieces, against one existing WP2 notebook.
- **D3.1** to medium: the National Society consultations (D2.3, Section 4.5, 6 of 11 conducted so far,
  strongly validating Use Cases 1 and 2) concluding on schedule, and at least one stable WP2 use-case
  notebook to train against.
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
