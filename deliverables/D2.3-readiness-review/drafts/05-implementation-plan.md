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
2. **Merge one of the CEMS or Charter `montandon-etl` integration PRs** (Section 4.2). Either one gives
   Use Case 2 a live event to validate against; CEMS is closer to merge-ready and is the more direct
   route.
3. **Run UC2 end to end against the resulting live event**, and get it reviewed by an IFRC or MapAction
   domain expert. This is the single most valuable step to move UC2 from built to validated before the
   meeting.
4. **Progress the database remediation** (Section 4.3) as far as staging-cluster access allows; at
   minimum, complete the index cleanup on the highest-bloat partitions, since this is the change most
   likely to visibly affect notebook responsiveness before the meeting.
5. **Bring forward early findings from the National Society interviews** (Section 4.5), even if the
   full interview round is not complete, so the Readiness Review discussion is grounded in what
   operational users have said so far.

## Short-term (through end of September 2026)

6. **Decide and communicate UC3's near-term scope** (Section 4.1): a full implementation, a defined
   narrower slice, or a specified-but-deferred status, so effort is not spent building against an
   unconfirmed target.
7. **If UC3 is in scope for a partial build**, start with the exposure × impact × vulnerability
   composite (reusing UC1 and UC2 outputs directly), deferring the historical-burden and
   operational-gap-and-accessibility components, both marked optional in the specification, to full WP2
   execution.
8. **Merge the second of the two CEMS/Charter integration PRs**, so both sources are loading into
   Montandon well ahead of December.
9. **Resolve the remaining database work**: complete the vacuum/reindex pass, apply the autoscaling
   settings tuned to the cleaned-up database, and revisit the `context=off` and write-load settings
   proposed during the investigation.

## WP2 execution (through December 2026)

10. **Complete the National Society interview round** and feed findings back into use-case refinement,
    particularly if any interviewed National Society flags a use case as lower-priority or surfaces a
    need the current three do not cover.
11. **Build out the historical-burden and operational-gap components of UC3**, if deferred per item 7,
    once UC1 and UC2 are stable and validated.
12. **Resolve the statistics-export question** (Section 4.4) as the aggregate-reporting need becomes
    concrete, most plausibly once `montandondata.org`'s public reporting requirements are firmer.

## Ownership

Database remediation is owned within the platform engineering effort, currently gated on staging-cluster
access; escalating that access is itself an action item for this plan. The CEMS and Charter
`montandon-etl` integrations each already have an assigned author and reviewer; merging them is a review
and testing task, not new design work. UC1 and UC2 notebook and application work is owned by MapAction,
with Development Seed supporting infrastructure and hosting. UC3 notebook development follows the same
pattern once started. A single decision-owner should be named for the baseline-computation strategy
(item 1) and the UC3 scope decision (item 6) at the Readiness Review meeting, since both are currently
open questions rather than assigned tasks.
