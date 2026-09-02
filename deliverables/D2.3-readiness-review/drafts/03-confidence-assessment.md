# Confidence Assessment

This section gives our honest assessment of confidence — not aspiration — for each use case reaching a
demonstrable state, and explains what that confidence is and is not based on.

| Use case | Build status | Confidence in reaching demonstrable state | Basis |
| --- | --- | --- | --- |
| UC1 — Risk Exposure | In progress; 3 of 4 hazards done, review in progress | **Medium-high** | Working notebooks and application exist today; remaining work (wildfire hazard, UX reconciliation) is well-scoped and additive, not architectural |
| UC2 — Impact Estimation | Initial implementation just opened | **Medium** | Follows a proven pattern from UC1, but unvalidated against a real event and unreviewed; too early in its cycle to rule out rework |
| UC3 — Response Prioritisation | Specification complete; build not started | **Medium-low** | Specification is strong, but the use case has not left the design phase, and inherits schedule risk from both UC1 and UC2 |

## Why confidence, not certainty

None of the three use cases carries **architectural** risk — the underlying pipeline, data model, and
correlation system are released and already load-bearing in the notebooks that exist. The uncertainty is
concentrated in **execution bandwidth and sequencing**: UC3 cannot be meaningfully validated until UC1
and UC2 produce stable, reviewed outputs to build on, and UC2 is itself only days into implementation.

We are confident that, at minimum, Use Case 1 can be shown working end-to-end by the Readiness Review
meeting. We are not confident that all three use cases will be demonstrable in equally finished form by
that date, and we think it is more useful to say so now than to imply otherwise. Section 5 sets out a
plan that prioritises getting Use Case 1 to a genuinely polished, user-testable state while making
visible, honest progress on Use Cases 2 and 3, rather than spreading effort thin across all three at
once.

## What would raise our confidence

- **UC1** → medium-high to high: wildfire hazard added, and a single decision made on the
  notebook-vs-Streamlit user experience (Section 4).
- **UC2** → medium to medium-high: one full run against a real, recent activation, reviewed by an IFRC
  or MapAction domain expert.
- **UC3** → medium-low to medium: UC2 validated, and an explicit scoping decision on how much of the
  prioritisation methodology is built and demonstrated now versus carried into full WP2 execution.

## What would lower it further

Continued database performance degradation (Section 4) is the single risk that could lower confidence
across all three use cases simultaneously, since every notebook queries the same Montandon STAC API for
its structured data. This is being actively worked but is not yet resolved, and we flag it accordingly
rather than assuming it away.
