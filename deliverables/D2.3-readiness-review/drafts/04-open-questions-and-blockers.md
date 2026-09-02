# Open Questions and Blockers

This section is deliberately candid: it lists what is unresolved, not just what is done. Some items are
scoping decisions we need from IFRC/ESA; others are engineering work already underway.

## 4.1 Use-case-specific

**UC1 — notebook vs. Streamlit, and the baseline-computation strategy.** Two parallel interfaces now
exist for risk exposure — a notebook series and a Streamlit application — and we have not yet decided
which is the primary, user-facing artefact (or whether both persist, for different audiences). This
connects to a bigger open question: because baseline risk exposure does not change often (it is not
event-driven, unlike Use Cases 2 and 3), it does not need to be recomputed live for every user. Three
options are on the table:

1. Keep computing on demand, per user selection (simplest, but repeats identical work).
2. Pre-compute on a schedule (e.g., yearly) for selected countries and hazards.
3. Pre-compute once for all countries, precisions, and hazards, and have notebooks reference the result
   rather than recompute it.

We are leaning toward option 2 or 3, which would also simplify the notebook-vs-Streamlit question (both
could read from the same precomputed, cloud-hosted dataset), but this needs a decision, not just a
preference — see Section 5.

**UC1 — wildfire hazard.** Data and methodology for the fourth hazard are not yet in hand; this is
tracked work, not an open design question.

**UC2 — unvalidated against a real event.** The initial implementation has not been run end-to-end
against a live or recent Copernicus EMS activation, nor reviewed by a domain expert. We treat this as
the single highest-priority gate before Use Case 2 can be called demonstrable.

**UC3 — scope at MTR.** The full response-prioritisation methodology (Section 2.3) is ambitious and
depends on two use cases that are not yet stable. We need an explicit decision on whether the Readiness
Review target is a full working implementation, a narrower slice (e.g., the exposure/impact/vulnerability
components only, without historical burden and operational-gap weighting), or a specified-but-not-built
status carried forward to full WP2 execution.

## 4.2 Cross-cutting: Montandon platform performance

The Montandon staging database has a real, actively-being-addressed performance problem that affects
every use case's notebooks, since all query the same STAC API. An initial investigation found the
~100 GB database bloated by duplicate property indexes (500+ redundant indexes on some source
partitions alone), caused by an indexing job that does not correctly detect existing indexes for
nested Monty fields. Basic autoscaling has been added, but further remediation — dropping the
duplicate indexes, vacuuming large partitions, and tuning memory settings — is blocked on staging-cluster
access for the engineer doing the work. Ownership is assigned and a plan exists; it is not yet complete.
We flag this because it is the one risk capable of degrading all three use cases simultaneously,
independent of their individual build progress.

## 4.3 Cross-cutting: statistics export format

A related, lower-urgency open question is how to export platform-wide statistics (event counts by
hazard type, and similar aggregate figures useful for public reporting and for `montandondata.org`) —
whether via a periodic GeoParquet export to cloud storage, or by querying the database directly. This
does not block any of the three use cases but does affect how their outputs might eventually be
aggregated and published at scale; a decision is pending.

## 4.4 Validation against real user needs

IFRC and MapAction are conducting structured interviews with National Society operations teams (Zambia,
Ethiopia, Kenya, Niger, Honduras, Chile, Netherlands, Denmark, Bangladesh, and the Philippines) through
August 2026, to validate that the three use cases as specified actually match operational need. This
work is in progress but not complete at the time of this report. We treat early, directional findings
from these interviews — where available — as more important to the Readiness Review discussion than
polish on any single notebook, since they test the premise the whole use-case series rests on.
