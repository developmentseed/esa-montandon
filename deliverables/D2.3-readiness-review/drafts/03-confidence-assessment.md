# Confidence Assessment

This section gives a factual assessment of confidence for each use case reaching a demonstrable state,
and the basis for that assessment.

**A note on how this is weighted.** Deliverable D2.4, where these use cases land as finished case
studies, is due in December 2026. At this checkpoint, whether every notebook is finished today is a
secondary signal; the primary ones are whether the design is sound, whether the dependencies it needs
are on track, and whether the remaining work is well-understood. A use case with a strong specification
and clear remaining steps is rated higher here than raw "lines of code shipped" would suggest.

| Use case | Build status | Confidence in reaching demonstrable state | Basis |
| --- | --- | --- | --- |
| UC1 — Risk Exposure | Built: 4 of 4 hazards, parameterised, published | **High** | Working, published notebooks exist today; the remaining baseline-compute decision is scoping, not engineering |
| UC2 — Impact Estimation | Built by MapAction, opened for review | **Medium-high** | Follows a proven, now twice-validated pattern from UC1; unvalidated against a real event, partly because CEMS/Charter data is not yet loading into Montandon |
| UC3 — Response Prioritisation | Specification complete and reviewed; build not started | **Medium** | No architecture risk and a strong specification; ample runway to December, but inherits sequencing risk from UC1 and UC2 |

## Basis for the assessment

None of the three use cases carries architectural risk: the underlying pipeline, data model, and
correlation system are released and already load-bearing in the notebooks that exist. What uncertainty
remains is concentrated in three places: getting real CEMS and Charter data flowing into Montandon,
a small number of open scoping decisions (Section 4), and the ordinary sequencing risk of UC3 depending
on UC1 and UC2.

Use Case 1 can reasonably be shown working end to end at the Readiness Review meeting; it already is,
in published form. Use Case 2 is close behind, gated mainly by real-event validation rather than by
anything still to design or build. Use Case 3 is earliest in its build cycle, but that is expected at
this point in the schedule and does not, on its own, lower confidence in it landing well ahead of
December.

## What would raise confidence

- **UC1** to very high: the baseline-computation strategy decided (Section 4).
- **UC2** to high: one of the CEMS or Charter `montandon-etl` integration PRs (Section 2.4) merged, and
  one full run against the resulting live event, reviewed by an IFRC or MapAction domain expert.
- **UC3** to medium-high: UC2 validated, and an explicit scoping decision on how much of the
  prioritisation methodology is built and demonstrated now versus carried into full WP2 execution.

## What would lower it

Continued production-database performance degradation ([issue #34](https://github.com/developmentseed/esa-montandon/issues/34))
is the one risk that could lower confidence across all three use cases simultaneously, since every
notebook queries the same Montandon STAC API for its structured data. Remediation is underway but not
complete. A prolonged delay in either the CEMS or Charter `montandon-etl` integration would similarly
hold back Use Case 2 and, in turn, Use Case 3.
