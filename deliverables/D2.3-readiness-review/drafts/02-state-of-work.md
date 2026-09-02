# State of Work

This section reports, for each use case, what has actually been built, against the D2.4 use-case
narrative and the D2.2 pipeline architecture it implements. Evidence is drawn from the repository's
pull-request and issue history as of early September 2026.

## 2.1 Use Case 1 — Population and Infrastructure Risk Exposure

**Status: in progress, furthest along of the three.**

MapAction delivered the baseline exposure-calculation methodology and an initial series of notebooks
covering three hazards (riverine flood, tropical cyclone, earthquake), shared in late July. This work
has since been ported into the project's notebook-hosting infrastructure and is being extended with
interactive visualisation and cascading-impact analysis.

In parallel, MapAction built a **Streamlit application** that wraps the same baseline exposure
calculation in a guided, parameter-driven interface — letting a user choose a country, administrative
precision, and hazard, and compute exposure without touching a notebook directly. That application is
open for review.

**What is missing:** wildfire exposure — the fourth of the four hazards specified for this use case —
has not yet been added; the tracking issue for the notebook work was explicitly reopened for this gap.
The Streamlit application and the notebook series have not yet been reconciled into a single, agreed
user experience — see the baseline-computation strategy question in Section 4, which affects how (and
how often) this use case's outputs are ultimately produced and published.

## 2.2 Use Case 2 — Post-disaster Impact Estimation

**Status: early — initial implementation just opened for review.**

An initial set of Jupyter notebooks implementing the impact-estimation methodology was opened for
review at the start of September, following the pattern established by Use Case 1: intersecting a
Copernicus EMS or Charter hazard footprint with population and infrastructure exposure layers for the
correlated event.

**What is missing:** this implementation has not yet been exercised end-to-end against a real,
recent disaster activation, nor reviewed by IFRC or MapAction domain experts. The temporal/monitoring
dimension described in the D2.4 narrative — re-running the analysis as new Copernicus EMS monitoring
products arrive for an evolving event — is not yet demonstrated. Because this use case is a direct
prerequisite for Use Case 3 (its output — observed impact — is one of Use Case 3's core inputs), its
timeline has a direct bearing on Use Case 3's.

## 2.3 Use Case 3 — Operational Response Prioritisation

**Status: fully specified, build not started.**

Unlike the other two, this use case's context, data sources, and methodology are already written up in
detail in the D2.4 narrative, including a worked, illustrative example against the 24 June 2026 La
Guaira (Venezuela) earthquake activation (Charter Act-1036 / EMSR894) and a proposed integration path
back into Charter client tools (a STAC `response-prioritisation` collection, a Charter Mapper overlay,
and a conversational client). This specification work is complete and reviewed.

**What is missing:** no notebook or pipeline implementation exists yet. This use case's core computation
— combining the exposure output of Use Case 1, the impact output of Use Case 2, INFORM vulnerability
data, and Montandon's historical/operational record into a composite, explainable prioritisation score
— is designed but unbuilt, and its two upstream dependencies are themselves still in progress (Sections
2.1–2.2). Several components described in the specification are explicitly marked as extensions beyond
current scope (notably, incorporating field observations via a planned IFRC Emergency Operations Centre
connection) and should not be read as MTR commitments.

## Cross-cutting foundation

All three use cases sit on the same foundation, which is not separately at risk: the Monty STAC
extension v1.3.0 (D1.1) and the event-correlation system (D2.1) are both released and in active use by
the notebooks above. The one shared foundation-level concern — Montandon staging-database performance —
is not use-case-specific and is discussed as a cross-cutting risk in Section 4, because it can affect
all three regardless of individual notebook progress.
