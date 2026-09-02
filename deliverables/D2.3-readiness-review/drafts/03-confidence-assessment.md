# Confidence Assessment

This section gives a factual assessment of confidence for each use case reaching a demonstrable state,
and the basis for that assessment.

| Use case | Build status | Confidence in reaching demonstrable state | Basis |
| --- | --- | --- | --- |
| UC1 — Risk Exposure | In progress; 3 of 4 hazards done, review in progress | **Medium-high** | Working notebooks and application exist today; remaining work (wildfire hazard, UX reconciliation) is well-scoped and additive, not architectural |
| UC2 — Impact Estimation | Initial implementation just opened | **Medium** | Follows a proven pattern from UC1, but unvalidated against a real event and unreviewed; too early in its cycle to rule out rework |
| UC3 — Response Prioritisation | Specification complete; build not started | **Medium-low** | Specification is strong, but the use case has not left the design phase, and inherits schedule risk from both UC1 and UC2 |

## Basis for the assessment

None of the three use cases carries architectural risk: the underlying pipeline, data model, and
correlation system are released and already load-bearing in the notebooks that exist. The uncertainty
is concentrated in execution bandwidth and sequencing. UC3 cannot be meaningfully validated until UC1
and UC2 produce stable, reviewed outputs to build on, and UC2 is only days into implementation.

Use Case 1 can reasonably be shown working end to end by the Readiness Review meeting. The other two are
unlikely to reach an equally finished state by that date. Section 5 sets out a plan that prioritises
getting Use Case 1 to a polished, user-testable state while making measurable progress on Use Cases 2
and 3, rather than spreading effort evenly across all three at once.

## What would raise confidence

- **UC1** to medium-high/high: wildfire hazard added, and a decision made on the notebook-vs-Streamlit
  user experience (Section 4).
- **UC2** to medium/medium-high: one full run against a real, recent activation, reviewed by an IFRC or
  MapAction domain expert.
- **UC3** to medium-low/medium: UC2 validated, and an explicit scoping decision on how much of the
  prioritisation methodology is built and demonstrated now versus carried into full WP2 execution.

## What would lower it

Continued database performance degradation (Section 4) is the one risk that could lower confidence
across all three use cases simultaneously, since every notebook queries the same Montandon STAC API for
its structured data. Remediation is underway but not complete.
