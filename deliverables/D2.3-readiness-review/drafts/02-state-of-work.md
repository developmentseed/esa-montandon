# State of Work

This section reports, for each use case, what has been built against the D2.4 use-case narrative and
the D2.2 pipeline architecture it implements, plus the state of the underlying CEMS and Charter data
pipelines both Use Case 2 and Use Case 3 depend on. Evidence is drawn from the pull-request and issue
history of the relevant repositories (`esa-montandon`, `manywidgets-playground`, `pystac-monty`,
`montandon-etl`) as of early September 2026.

## 2.1 Use Case 1 — Population and Infrastructure Risk Exposure

**Status: built and published; refinement in progress.**

MapAction delivered the baseline exposure-calculation methodology and an initial series of notebooks
covering three hazards (riverine flood, tropical cyclone, earthquake), shared in late July. Wildfire, the
fourth specified hazard, has since been added, so all four hazards specified for this use case are now
covered.

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
case's outputs are computed and published, independent of interface.

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
EMS monitoring products arrive for an evolving event, is not yet demonstrated. Because this use case is
a direct prerequisite for Use Case 3 (its output, observed impact, is one of Use Case 3's core inputs),
its timeline has a direct bearing on Use Case 3's.

## 2.3 Use Case 3 — Operational Response Prioritisation

**Status: fully specified, build not started.**

Unlike the other two, this use case's context, data sources, and methodology are already written up in
detail in the D2.4 narrative, including a worked, illustrative example against the 24 June 2026 La
Guaira (Venezuela) earthquake activation (Charter Act-1036 / EMSR894) and a proposed integration path
back into Charter client tools: a STAC `response-prioritisation` collection, a Charter Mapper overlay,
and a conversational client. This specification work is complete and reviewed.

**What remains.** No notebook or pipeline implementation exists yet, which is expected this far ahead of
the December D2.4 deadline. This use case's core computation, combining the exposure output of Use Case
1, the impact output of Use Case 2, INFORM vulnerability data, and Montandon's historical/operational
record into a composite, explainable prioritisation score, is designed but unbuilt, and its two upstream
dependencies are themselves still in progress (Sections 2.1–2.2). Several components described in the
specification are marked as extensions beyond current scope (notably, incorporating field observations
via a planned IFRC Emergency Operations Centre connection) and should not be read as MTR commitments.

## 2.4 CEMS and Charter ETL pipelines

Use Cases 2 and 3 both depend on Copernicus EMS and International Charter hazard and response data being
loaded into Montandon. This is not yet the case, though both pipelines are in active development.

**Copernicus EMS.** The transformer that converts CEMS Rapid Mapping products into Monty STAC items is
implemented and merged in `pystac-monty`, and has received several rounds of fixes this past week
(correcting related-item links and relaxing overly strict event matching). Deploying it as a running
pipeline is in progress: the integration PR in `montandon-etl` has been open since 10 August 2026 and is
not yet merged, so CEMS activations are not yet being ingested into the live Montandon STAC API.

**International Charter.** The transformer is implemented and merged in `pystac-monty`, built against a
detailed, reviewed implementation specification. As with CEMS, the `montandon-etl` integration PR is
still a draft, open since 26 June 2026, so Charter data is likewise not yet loading into Montandon.

**What this means for Use Cases 2 and 3.** Both use cases can be developed and unit-tested against the
worked examples already in `monty-stac-extension` (real CEMS and Charter fixtures used to build and
validate the transformers), but cannot yet be run against a live, currently-correlated Montandon event
until one of the two `montandon-etl` integration PRs merges. This is the most direct near-term dependency
for validating Use Case 2 end to end (Section 4.1) and, in turn, for Use Case 3.

## Cross-cutting foundation

All three use cases sit on the same foundation, which is not separately at risk: the Monty STAC
extension v1.3.0 (D1.1) and the event-correlation system (D2.1) are both released and in active use by
the notebooks above. The one shared foundation-level concern, Montandon production-database performance,
is not use-case-specific and is discussed as a cross-cutting risk in Section 4, since it can affect all
three regardless of individual notebook progress.
