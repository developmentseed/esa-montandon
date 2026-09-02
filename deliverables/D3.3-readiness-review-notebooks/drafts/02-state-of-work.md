# State of Work

## 2.1 Notebook-publishing architecture (D3.3 core)

**Status: architecture proposed and discussed; core pattern already validated by WP2; Django
implementation not started.**

The proposed design was written up in detail by the team, grounded in the original MapAction use-cases
document and iterated into a walkthrough site outlining the architecture end to end. The tracking issue
remains open with no linked Django/Celery implementation work.

The proposed architecture is:

- A **Django application** as the orchestration and indexing layer. It stores lightweight metadata
  (which notebook, which parameters, who ran it, when) but not notebook content itself.
- A **Celery worker queue**, so triggering a run does not block the user. A job is queued, executed, and
  its result recorded.
- **papermill** to execute the chosen notebook template with the user-supplied parameters, following
  the same pattern WP2's automated pipeline already uses for event-triggered runs.
- Rendering to **static HTML** (via MyST), published to **object storage**, so that browsing a finished
  analysis is a cheap, cacheable static-file fetch rather than a live app request.
- **Kubernetes** for execution, reusing the same job-based, resource-bounded execution pattern already
  operating in WP2's pipeline.

This design does not introduce new infrastructure. It composes Django, Celery, and Kubernetes, all
either already used elsewhere in this stack or standard, well-understood tools, around the same
notebook-as-interchangeable-object model WP2 already validated. Of the three use cases (risk exposure,
impact estimation, response prioritisation; see D2.3), Use Case 1 and Use Case 2 are already built and
map directly onto this platform as templates; Use Case 3 will follow once built.

**Proof of concept, already in production.** The core user-facing pattern this platform is meant to
generalise, parameterise a notebook, run it via papermill, publish the result as static HTML, is not
hypothetical: WP2's Use Case 1 notebooks already work exactly this way. The data-preparation,
exposure-calculation, and visualisation notebooks take a country parameter and run end to end via
papermill, validated for more than one country, and the output is published to a live MyST site
(D2.3, Section 2.1). This de-risks the platform's central mechanism well ahead of building the Django
orchestration layer around it. An earlier Streamlit prototype explored a guided-form interface for the
same use case but is not expected to carry forward.

**What remains.** The Django orchestration layer itself: no Django project, Celery configuration, or
authoring UI exists yet. Four specific design questions remain open (Section 4) and should be resolved
before significant engineering investment, since they affect the shape of the data model and the compute
strategy.

## 2.2 Training material for relevant user communities (D3.1)

**Status: not started; scheduled to begin October 2026.**

MapAction, who own this deliverable, have stated that training material development will start once the
National Society consultations (D2.3, Section 4.5) conclude and the first user-facing notebooks and
tools have a first working version. This is a sensible sequencing choice; training material built
against an unstable interface would need rework. It does mean D3.1 has no content yet.

## 2.3 Technical documentation for integration into ESA JupyterLab environments (D3.2)

**Status: not started.**

This deliverable is assigned but has no visible work product yet. It is also the WP3 deliverable most
directly gated by D3.3: it cannot document an integration path into ESA JupyterLab environments until
the notebook-publishing platform's own architecture is at least partially implemented and its
notebook/environment contract is stable.

## 2.4 Report of the demonstration of the analytics services with IFRC users (D3.4)

**Status: not started.**

This deliverable is last in WP3's dependency chain. A demonstration presupposes a working platform
(D3.3), material to train users on it (D3.1), and, ideally, documentation of how it fits ESA's tooling
(D3.2). No demonstration activity has begun.

## 2.5 Adjacent capabilities already in place

Two pieces of related infrastructure, while not formal WP3 deliverables, reduce the risk of the plan in
Section 5 and are worth noting:

- **Visualisation.** WP2's pipeline design already commits to TiTiler, Development Seed's open-source
  dynamic tiling server, for rendering EO and derived raster layers on the fly. WP3's interactive tools
  reuse this rather than building new visualisation infrastructure, a proven, low-risk component
  already operating elsewhere in the Montandon stack.
- **LLM-driven / conversational access.** A separate, already-functioning capability, an MCP (Model
  Context Protocol) service exposing Montandon's event, hazard, and impact data for natural-language
  querying, has been built and deployed, evolved from an earlier Claude-Code-specific skill pack into a
  standard toolset served on Kubernetes. This is not currently scoped as a formal WP3 sub-deliverable,
  but it demonstrates a second, complementary "interactive access" pattern alongside the Django
  platform, and is worth including in the WP3 narrative for the Readiness Review meeting as evidence of
  momentum on the access-patterns side of this work package.
