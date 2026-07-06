# Reference Architecture

The pipeline is an **event-driven architecture**: monitoring services watch upstream data sources, an
orchestration layer correlates and queues new events, a compute layer runs the appropriate analysis on
a Kubernetes cluster, and the resulting artifacts are published to cloud storage and surfaced in IFRC
GO. The stages are shown below.

![The event-driven pipeline: monitoring services detect new data; the orchestration layer correlates (D2.1) and queues each event; the Kubernetes compute layer runs the appropriate notebooks from the code repositories; and the artifacts are published to cloud storage and IFRC GO.](pipeline-architecture.png)

## Stage-by-stage

| Stage | Responsibility | Key components |
| --- | --- | --- |
| Monitoring & data systems | Detect new disaster data | Copernicus EMS RSS feed, Montandon STAC API, UNOSAT API |
| Event orchestration | Detect, correlate, and queue events | Listener/poller, correlation logic (D2.1), message queue / event bus |
| Compute | Run the right analysis on demand | Kubernetes job controller, notebook execution pods (papermill) |
| Code & analysis repos | Supply analysis logic | `pystac-monty`, modular notebook suite |
| Outputs | Publish decision-ready results | Cloud storage, IFRC GO platform |

## How a single event flows through

1. A **monitoring service** detects new upstream data — a Copernicus EMS activation appears on the RSS
   feed, or a new event lands in Montandon.
2. The **listener** picks it up and hands it to the **correlation logic** (D2.1), which attaches the EO
   hazard layer to the correct event, hazard, and impact records and assembles the complete data context
   for that disaster.
3. The correlated event is placed on a **message queue**, which triggers a job via the **Kubernetes job
   controller**. The job selects the analyses to run from an analysis matrix keyed on hazard type and
   available data (Section 6).
4. A **notebook execution pod** runs the selected notebook(s) with papermill, parameterised for the
   specific country and event, pulling structured data and EO layers through `pystac-monty`.
5. The **artifacts** produced — static HTML, PDF, JSON, and map layers — are uploaded to **cloud
   storage** and linked from the **IFRC GO** platform, where they feed the DREF workflow.

## Why this shape

The event-driven, queue-decoupled design means each stage scales and fails independently: many events
can be processed concurrently; a slow or failed analysis does not block ingestion; and new analyses are
added by registering a notebook rather than modifying the orchestration. Running analyses as isolated
Kubernetes jobs gives reproducible, resource-bounded execution per event. The following sections detail
the modular analytics model (Section 4), the data-combination it performs (Section 5), and the
orchestration logic (Section 6).
