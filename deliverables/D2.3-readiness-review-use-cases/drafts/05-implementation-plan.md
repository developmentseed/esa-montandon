# Implementation Plan

This plan sequences the work needed to move each use case from its current state (Section 2) to a
demonstrable one, and resolves the open questions in Section 4 where they gate that work. Items are
grouped by urgency relative to the Readiness Review meeting on 14 September 2026, not by the December
D2.4 deadline; several items are intentionally left for WP2 execution rather than rushed into the MTR
window, since there is runway to do them properly.

## Immediate (before the Readiness Review meeting)

1. **Decide the baseline-computation strategy for UC1** (Section 4.1). Option 2 or 3 (scheduled or full
   pre-computation, published to cloud storage) is recommended over recomputing on demand, since a
   pre-computed dataset is cheaper to serve and keeps published outputs consistent. This is a decision,
   not new engineering, and should be made this week.
2. **Confirm Copernicus EMS reaches production** (Section 4.2). Staging is done; production deployment
   is in progress with no confirmed date yet. Charter is still targeting staging, expected around
   17 September 2026.
3. **Run UC2 end to end against the resulting live event**, now that CEMS is live on staging (or once
   Charter is), and get it reviewed by an IFRC or MapAction domain expert. This is the single most
   valuable step to move UC2 from built to validated before the meeting.
4. **Progress the database remediation** (Section 4.3) as far as staging-cluster access allows; at
   minimum, complete the index cleanup on the highest-bloat partitions, since this is the change most
   likely to visibly affect notebook responsiveness before the meeting.
5. **Bring forward the National Society interview findings to date** (Section 4.5): 6 of 11 planned
   interviews conducted, with results so far strongly validating Use Cases 1 and 2. This is a
   substantive, positive signal worth featuring at the meeting, not merely a status update.

## Short-term (through end of September 2026)

6. **Communicate UC3's reframed near-term scope** (Section 4.1) to stakeholders: an externally-led,
   best-effort Utility Report rather than a build or an informal review, so effort is not spent on
   implementation the plan no longer calls for at this stage.
7. **Finalise engagement terms with UNOSAT** for the Nepal activation: agree best-effort, non-committal
   terms and Montandon access so they can start producing the Utility Report, and confirm separately
   whether the activation's Red Cross/Red Crescent involvement allows the added National Society
   linkage.
8. **Confirm Charter reaches staging** (the second of the two CEMS/Charter ETL pipelines), so both
   sources are loading into Montandon well ahead of December. Separately, deploy the pending
   `pystac-monty` versioning changes to PROD and progress
   [monty-stac-extension#147](https://github.com/IFRCGo/monty-stac-extension/issues/147) (the eoAPI
   queryables version field).
9. **Resolve the remaining database work**: complete the vacuum/reindex pass, apply the autoscaling
   settings tuned to the cleaned-up database, and revisit the `context=off` and write-load settings
   proposed during the investigation.

## WP2 execution (through December 2026)

10. **Complete the National Society interview round** and feed findings back into use-case refinement,
    particularly if any interviewed National Society flags a use case as lower-priority or surfaces a
    need the current three do not cover.
11. **Build out the composite-score implementation for UC3**, informed by the Utility Report's findings
    (item 7), once UC1 and UC2 are stable and validated. This remains longer-term WP2 execution work
    with no near-term date.
12. **Resolve the statistics-export question** (Section 4.4) as the aggregate-reporting need becomes
    concrete, most plausibly once `montandondata.org`'s public reporting requirements are firmer.

## Ownership

Database remediation is owned within the platform engineering effort, currently gated on staging-cluster
access; escalating that access is itself an action item for this plan. The CEMS and Charter
`montandon-etl` integrations each already have an assigned author and reviewer; completing CEMS's
production deployment and Charter's staging deployment is a review and testing task, not new design
work. UC1 and UC2 notebook and application work is owned by MapAction, with Development Seed supporting
infrastructure and hosting. UC3's eventual composite-score build follows the same pattern once started;
its near-term Utility Report is owned by the ESA project manager, who has selected UNOSAT for the
current Nepal activation. A single decision-owner should be named for the baseline-computation strategy
(item 1) at the Readiness Review meeting, since it is the one major open question remaining; UC3's
near-term approach (item 6) is decided, with UNOSAT and Nepal confirmed as partner and activation
(Section 2.3); finalising engagement terms (item 7) is the only open step.
