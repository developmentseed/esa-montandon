# Confidence Assessment

This section gives a factual assessment of confidence for each use case reaching a demonstrable state,
and the basis for that assessment.

**A note on how this is weighted.** Deliverable D2.4, where these use cases land as finished case
studies, is due in December 2026. At this checkpoint, whether every notebook is finished today is a
secondary signal; the primary ones are whether the design is sound, whether the dependencies it needs
are on track, and whether the remaining work is well-understood. A use case with a strong specification
and clear remaining steps is rated higher here than raw "lines of code shipped" would suggest.

| Use case                | Build status                                                                                                     | Confidence in reaching demonstrable state | Basis                                                                                                                                                   |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| UC1 — Risk Exposure     | Built: 3 of 4 hazards, parameterised, published                                                                  | **High**                                  | Working, published notebooks exist today; the remaining baseline-compute decision is scoping and notebook design                                        |
| UC2 — Impact Estimation | Built by MapAction, opened for review                                                                            | **Medium-high**                           | Follows a proven, now twice-validated pattern from UC1; unvalidated against a real event, partly because CEMS/Charter data is not yet on staging        |
| UC3 — Utility Report    | Reframed as an externally-led Utility Report (best-effort, non-committal); partner onboarding not yet finalised. | **Medium-high**                           | No engineering risk and no dependency on UC1/UC2 or the CEMS/Charter timeline; the only real uncertainty is whether a best-effort, uncommitted delivers |

## Basis for the assessment

None of the three use cases carries architectural risk: the underlying pipeline, data model, and
correlation system are released and already load-bearing in the notebooks that exist. What uncertainty
remains is concentrated in three places: getting real CEMS and Charter data flowing into Montandon
(which now affects only UC2), a small number of open scoping decisions (Section 4), and confirming UC3's
external partner and activation.

Use Case 1 can reasonably be shown working end to end at the Readiness Review meeting; it already is,
in a published form. However, use case one is still in a "proof of concept" state and requires refinement. Use Case 2 is close behind, gated mainly by real-event validation rather than by
anything substantial to build. Use Case 3 is no longer on a build cycle for this near-term
checkpoint at all: its reframed near-term form is an external partner's assessment of Montandon,
decoupled from UC1/UC2 status and from the CEMS/Charter ETL timeline. This removes most of the
sequencing risk the earlier framing carried; what remains is confirming a partner and activation, and
the inherent uncertainty of a best-effort, non-committal engagement.

## What would raise confidence

- **UC1** to very high: the baseline-computation strategy decided (Section 4).
- **UC2** to high: CEMS or Charter production (Section 2.4), and one full run against the
  resulting live event, reviewed by an IFRC or MapAction domain expert.
- **UC3** to high: a partner and Charter activation confirmed,
  and the Utility Report received.
