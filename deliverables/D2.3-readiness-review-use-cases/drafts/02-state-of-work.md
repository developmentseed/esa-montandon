# State of Work

This section reports, for each use case, what has been built against the D2.4 use-case narrative and
the D2.2 pipeline architecture it implements, plus the state of the underlying CEMS and Charter data
pipeline Use Case 2 depends on. Evidence is drawn from the engineering and issue history of the relevant
repositories (`esa-montandon`, `manywidgets-playground`, `pystac-monty`, `montandon-etl`) as of early
September 2026, plus other communication channels.

## 2.1 Use Case 1 — Population and Infrastructure Risk Exposure

**Status: built and published; refinement in progress.**

MapAction delivered the baseline exposure-calculation methodology and an initial series of notebooks
covering three hazards (riverine flood, tropical cyclone, earthquake), shared in late July. Wildfire, the
fourth specified hazard, is currently under development.

The notebooks were also parameterised so a single notebook template runs for any country, rather than
being hand-edited per country: the data-preparation, population-exposure, infrastructure-exposure, and
visualisation notebooks now take a country parameter and run end to end via papermill (validated against
Kenya, alongside the original example country). This is a working, real-world instance of the
parameterised-notebook pattern that both the D2.2 pipeline and the D3.3 notebook-publishing platform are
built around. The result is published as a working example at
[manywidgets-playground/monty-use-case-1](https://developmentseed.org/manywidgets-playground/monty-use-case-1/),
showing baseline hazard exposure for a country's population against all four hazards.

MapAction earlier prototyped a Streamlit application wrapping the same calculation in a guided,
parameter-driven form. That exploration informed the current direction, but the notebook-and-published-site
path above is the one being carried forward; Streamlit is not expected to be the long-term interface.

**What remains.** The baseline-computation strategy question in Section 4: how, and how often, this use
case's outputs are computed and published, independent of interface. Separately, while the
parameterised-notebook and publishing pattern is proven and stress-tested, for example the Kenya instance
at [manywidgets-playground/data-visualization-ken](https://developmentseed.org/manywidgets-playground/data-visualization-ken/),
the notebook's own content is still rough and will need to be recreated to be more polished and
impactful. That is a content gap, not an architecture risk.

## 2.2 Use Case 2 — Post-disaster Impact Estimation

**Status: initial implementation built by MapAction, opened for review.**

An initial set of Jupyter notebooks implementing the impact-estimation methodology, built by MapAction,
was opened for review at the start of September, following the pattern established by Use Case 1:
intersecting a Copernicus EMS or Charter hazard footprint with population and infrastructure exposure
layers for the correlated event.

**What remains.** This implementation has not yet been run end to end against a real, recent disaster
activation, nor reviewed by IFRC or MapAction domain experts. Doing so also depends on Copernicus EMS
and Charter data actually being loaded into Montandon, which is not yet the case (Section 2.4). The
temporal/monitoring dimension described in the D2.4 narrative, re-running the analysis as new Copernicus
EMS monitoring products arrive for an evolving event, is not yet demonstrated. This use case's output
would be a direct input to Use Case 3's eventual composite score (Section 2.3), so its timeline still has
a bearing on that longer-term build; it has no bearing on Use Case 3's near-term Utility Report activity,
which is independent of UC1/UC2 status.

## 2.3 Use Case 3 — Utility Report

**Status: reframed for this cycle as an externally-led Utility Report rather than a build; partner and
activation decided (UNOSAT, Nepal), engagement terms being finalised.**

The full response-prioritisation methodology, its data sources, and a worked example are already
written up in detail in the D2.4 narrative, including an illustrative worked example against the
24 June 2026 La Guaira (Venezuela) earthquake activation (Charter Act-1036 / EMSR894) and a proposed
integration path back into Charter client tools: a STAC `response-prioritisation` collection, a Charter
Mapper overlay, and a conversational client. This specification work is complete and reviewed, and
remains the longer-term direction, but is no longer the near-term target for this use case.

The near-term plan has changed substantially. Rather than building the composite score, the
proposal from ESA is to engage a third-party partner already active in a Charter
activation to assess Montandon directly. The engagement is explicitly best-effort and non-committal: the
partner would use the Montandon database, irrespective of whether Charter-sourced content is itself in
Montandon, alongside their own work on a live Charter activation, and produce a Utility Report assessing
the relevance and fitness for purpose of Montandon's data for that work, with recommendations for future
improvement. Because there is no delivery obligation on either side, this carries very little execution
risk for WP2, at the cost of no firm date for the report itself.

**UNOSAT, Nepal.** The partner and activation are effectively decided: UNOSAT, as Charter Project
Manager for the current large-scale ("mega") activation in Nepal. What remains is agreeing engagement
terms and Montandon access, not selecting a partner. Whether this activation also involves Red Cross or
Red Crescent, which would additionally allow linking National Society engagement to the results, is
still being explored, potentially as part of a separate Montandon enhancement activity. This will be
discussed at the Readiness Review meeting in Geneva on 14 September.

**What remains.** Agreeing terms for the (non-committal) engagement and Montandon access with UNOSAT.
The composite-score implementation itself, combining the exposure output of Use Case 1, the
impact output of Use Case 2, INFORM vulnerability data, and Montandon's historical/operational record,
remains designed but unbuilt, and is no longer tied to a near-term date; it is longer-term WP2 execution
work, to be revisited in light of whatever the Utility Report finds. Several components described in the
specification are marked as extensions beyond current scope (notably, incorporating field observations
via a planned IFRC Emergency Operations Centre connection) and should not be read as MTR commitments.

## 2.4 CEMS and Charter ETL pipelines

Use Case 2 depends on Copernicus EMS and International Charter hazard and response data being loaded
into Montandon. Copernicus EMS has now reached staging; Charter has not yet, though it is close, and
neither is yet in production. Use Case 3, in its near-term, externally-led form (Section 2.3), does not depend on
this: the proposed partner engagement is explicitly designed to use Montandon's database irrespective of
whether Charter-sourced content is itself present.

**Copernicus EMS.** The transformer that converts CEMS Rapid Mapping products into Montandon STAC items is
implemented and merged in `pystac-monty`, and has received several rounds of fixes this past week
(correcting related-item links and relaxing overly strict event matching). CEMS data is now flowing on
staging. Production deployment is still in progress, with no confirmed date yet.

**International Charter.** The transformer is implemented and merged in `pystac-monty`, built against a
detailed, reviewed implementation specification. The `montandon-etl` integration, under way since 26 June
2026, is progressing toward a staging deployment expected roughly a week after CEMS, around
17 September 2026.

**pystac-monty versioning.** Separately from the CEMS/Charter transformers, a small number of
`pystac-monty` changes, including item versioning, are implemented but not yet deployed to PROD.
Versioning lets a Monty STAC item record which version of the transformer produced it, which matters for
reproducibility as transformers keep changing. A follow-on piece of work, adding the version field to
eoAPI's queryables so it can be used as a search filter, is tracked as
[monty-stac-extension#147](https://github.com/IFRCGo/monty-stac-extension/issues/147).

**What this means for Use Case 2.** It can be developed and unit-tested against the worked examples
already in `monty-stac-extension`. With CEMS now on staging, it can be run there against a live,
currently-correlated Montandon event; a full production run awaits CEMS's production deployment.
Charter-sourced events remain unavailable until Charter reaches staging (expected mid-to-late September
2026). This is the most direct near-term dependency for validating Use Case 2 end to end (Section 4.1).
Use Case 3's near-term Utility Report activity (Section 2.3) has no such dependency.

## Cross-cutting foundation

All three use cases sit on the same foundation, which is not separately at risk: the Monty STAC
extension v1.3.0 (D1.1) and the event-correlation system (D2.1) are both released and in active use by
the notebooks above. The one shared foundation-level concern, Montandon production-database performance,
is not use-case-specific and is discussed as a cross-cutting risk in Section 4, since it can affect all
three regardless of individual notebook progress.
