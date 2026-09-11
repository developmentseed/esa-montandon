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
| UC2 — Impact Estimation | Built by MapAction, opened for review | **Medium-high** | Follows a proven, now twice-validated pattern from UC1; unvalidated against a real event, partly because CEMS/Charter data is not yet on staging (CEMS hoped ~11 Sept 2026, Charter ~1 week later) |
| UC3 — Response Prioritisation | Reframed as an externally-led Utility Report (best-effort, non-committal); partner/activation not yet finalised, UNOSAT/Nepal leading candidate | **Medium-high** | No engineering risk and no dependency on UC1/UC2 or the CEMS/Charter timeline; the only real uncertainty is whether a best-effort, uncommitted partner confirms and delivers |

## Basis for the assessment

None of the three use cases carries architectural risk: the underlying pipeline, data model, and
correlation system are released and already load-bearing in the notebooks that exist. What uncertainty
remains is concentrated in three places: getting real CEMS and Charter data flowing into Montandon
(which now affects only UC2), a small number of open scoping decisions (Section 4), and confirming UC3's
external partner and activation.

Use Case 1 can reasonably be shown working end to end at the Readiness Review meeting; it already is,
in published form. Use Case 2 is close behind, gated mainly by real-event validation rather than by
anything still to design or build. Use Case 3 is no longer on a build cycle for this near-term
checkpoint at all: its reframed near-term form is an external partner's assessment of Montandon,
decoupled from UC1/UC2 status and from the CEMS/Charter ETL timeline. This removes most of the
sequencing risk the earlier framing carried; what remains is confirming a partner and activation, and
the inherent uncertainty of a best-effort, non-committal engagement.

## What would raise confidence

- **UC1** to very high: the baseline-computation strategy decided (Section 4).
- **UC2** to high: CEMS or Charter reaching staging (Section 2.4), and one full run against the
  resulting live event, reviewed by an IFRC or MapAction domain expert.
- **UC3** to high: a partner and Charter activation confirmed (UNOSAT/Nepal is the leading candidate),
  and the Utility Report received.

## What would lower it

Continued production-database performance degradation ([issue #34](https://github.com/developmentseed/esa-montandon/issues/34))
is the one risk that could lower confidence across all three use cases simultaneously, since every
notebook queries the same Montandon STAC API for its structured data. Remediation is underway but not
complete. A delay beyond the expected mid-September staging dates for CEMS or Charter would hold back
Use Case 2; it would no longer affect Use Case 3, which is now independent of this timeline. For Use
Case 3 specifically, the main risk is failing to confirm a suitable partner and activation, or the
partner declining to engage once approached, though this was priced in from the outset given the
engagement's non-committal nature.
