# Conclusion and Next Steps

## Assessment outcome

WP2's architecture is sound and delivered (D2.1, D2.2). Execution is ahead of what a first read of the
pull requests alone would suggest: Use Case 1 is built, parameterised, and published; Use Case 2 is
built and awaiting real-event validation; Use Case 3 is well-specified and, while unbuilt, has ample
runway to the December D2.4 deadline. The main items standing between today and a fully demonstrated set
of case studies are a handful of decisions and one piece of integration work (getting CEMS or Charter
data loading into Montandon), not open design questions.

## Topics for the Readiness Review meeting

- The baseline-computation strategy decision for Use Case 1 (Section 4.1, Section 5 item 1). This
  should be resolved at or before the meeting, since it is blocking and cheap to decide.
- Merging the CEMS or Charter `montandon-etl` integration (Section 4.2, Section 5 item 2), since it is
  the fastest path to a real-event validation of Use Case 2.
- The scope of Use Case 3 for this milestone (Section 4.1, Section 5 item 6): whether a partial build,
  a full build, or a specified-but-deferred status is the right near-term target, given the December
  deadline.
- Early signal from the National Society interviews (Section 4.5), to ground the discussion in
  operational user feedback alongside the internal assessment.
- Status and timeline of the database remediation (Section 4.3), since it is the one risk that could
  affect all three use cases regardless of individual progress.

## Path to D2.4

This report is a checkpoint, not the finish line, and D2.4 is not due until December 2026. Use Case 1 is
close to demonstration-ready today. Use Case 2 needs a live event to validate against, which is close at
hand once one of the two ETL integrations merges. Use Case 3's strong specification gives it a clear
starting point once its dependencies are stable. The plan in Section 5 is scoped to keep that trajectory
on track without forcing any use case ahead of where its dependencies allow.
