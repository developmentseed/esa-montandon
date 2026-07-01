# Event-Driven Orchestration

The orchestration layer turns the arrival of new data into the right analysis, automatically. This
section documents its logic at architecture level.

## Trigger sources

The pipeline listens to several upstream streams, each signalling that new analysis may be warranted:

- **Copernicus EMS RSS feed** — a new Rapid Mapping activation or product. This is the primary EO
  trigger and the same feed serves both WP1 ingestion and this WP2 orchestration.
- **Montandon** — a new or updated event in the crisis data bank (itself fed by GDACS, EM-DAT, and other
  sources), signalling a disaster that may warrant analysis even before an EO product exists.
- **UNOSAT API** — new humanitarian mapping products.

A lightweight **listener/poller** service watches these streams and normalises each signal into a
candidate analysis event.

## Correlation and queuing

Each candidate event passes through the **correlation logic** (D2.1), which attaches any EO hazard layer
to the correct event, hazard, and impact records and assembles the data context. Correlated events are
placed on a **message queue / event bus**, decoupling detection from computation so that bursts of
activity (many simultaneous disasters) are absorbed and processed in order without overloading the
compute layer.

## The analysis matrix

Which analyses run for a given event is governed by an **analysis matrix** — a configuration, defined
with MapAction's operational input, that maps the event's characteristics to the notebooks to execute:

| Determinant | Example | Effect |
| --- | --- | --- |
| Hazard type | Flood / wildfire / earthquake / cyclone | Selects the hazard-appropriate exposure and damage notebooks |
| Available EO product | Delineation vs. grading present | Enables exposure vs. damage analyses accordingly |
| Available exposure data | Population / infrastructure layers present | Determines which targets can be estimated |

The matrix is data, not code: adding a hazard/analysis combination is a configuration change plus the
registration of a notebook (Section 4), keeping the orchestration stable.

## Job lifecycle

For each queued event, the **Kubernetes job controller** launches a job that:

1. resolves the notebooks to run from the analysis matrix;
2. starts a **notebook execution pod** that runs each notebook with papermill, parameterised for the
   country and event, pulling data through `pystac-monty` and the STAC API;
3. collects the outputs; and
4. terminates, releasing resources.

Running each analysis as an isolated, resource-bounded job gives reproducible execution and independent
failure — one event's analysis cannot disrupt another's.

![From alert to artifact: a new event is correlated to its data context (D2.1), the analysis matrix selects the notebooks to run, the Kubernetes job performs the footprint-versus-exposure analysis, and the outputs are published to IFRC GO.](event-to-artifact.png)

## Artifact publishing

The outputs — static HTML reports, PDFs, JSON, and map layers — are uploaded to **cloud storage** and
**linked from IFRC GO**, where they feed the DREF preparation workflow and can be surfaced on the
emergency page. Because each artifact is tied to the event's correlation identifier, it is unambiguously
associated with its disaster. The pipeline is built to add, edit, and re-trigger analyses easily, so the
catalog of automated outputs grows over time.
