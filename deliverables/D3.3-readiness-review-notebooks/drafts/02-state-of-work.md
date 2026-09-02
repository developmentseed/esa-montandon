# State of Work

## 2.1 Notebook-publishing architecture (D3.3 core)

**Status: architecture proposed and discussed; no implementation started.**

The proposed design was written up in detail by the team, grounded in the original MapAction use-cases
document and iterated into a walkthrough site outlining the architecture end-to-end. It has not yet had
dedicated engineering time; the tracking issue remains open with no linked implementation work.

The proposed architecture is:

- A **Django application** as the orchestration and indexing layer — it stores lightweight metadata
  (which notebook, which parameters, who ran it, when) but not notebook content itself.
- A **Celery worker queue**, so triggering a run does not block the user — a job is queued, executed,
  and its result recorded.
- **papermill** to execute the chosen notebook template with the user-supplied parameters, exactly as
  WP2's automated pipeline already does for event-triggered runs.
- Rendering to **static HTML** (via MyST), published to **object storage** — so that browsing a
  finished analysis is a cheap, cacheable static-file fetch, not a live app request.
- **Kubernetes** for execution, reusing the same job-based, resource-bounded execution pattern already
  operating in WP2's pipeline.

This is a deliberate, and we think correct, design choice: it does not introduce new infrastructure. It
composes Django, Celery, and Kubernetes — all either already used elsewhere in this stack or
standard, well-understood tools — around the same notebook-as-interchangeable-object model WP2 already
validated. The three use cases (risk exposure, impact estimation, response prioritisation — see D2.3)
map directly onto this platform as the initial set of "official" templates.

**Early proof of concept.** MapAction's Streamlit application for Use Case 1 (see D2.3, Section 2.1),
while built independently of this architecture, already demonstrates the core user-facing pattern this
platform is meant to generalise — select parameters, trigger a computation, get a usable output — and is
a useful reference implementation as the Django platform is built.

**What is missing:** an actual implementation. No Django project, Celery configuration, or authoring UI
exists yet. Four specific design questions remain open (Section 4) and should be resolved before
significant engineering investment, since they affect the shape of the data model and the compute
strategy.

## 2.2 Training material for relevant user communities (D3.1)

**Status: not started; explicitly scheduled to begin October 2026.**

MapAction, who own this deliverable, have stated that training material development will start once the
National Society consultations (D2.3, Section 4.4) conclude and the first user-facing notebooks and
tools have a first working version. This is a deliberate, sensible sequencing choice — training material
built against an unstable interface would need rework — but it does mean D3.1 has no content yet.

## 2.3 Technical documentation for integration into ESA JupyterLab environments (D3.2)

**Status: not started.**

This deliverable is assigned but has no visible work product yet. It is also the WP3 deliverable most
directly gated by D3.3: it cannot meaningfully document an integration path into ESA JupyterLab
environments until the notebook-publishing platform's own architecture is at least partially
implemented and its notebook/environment contract is stable.

## 2.4 Report of the demonstration of the analytics services with IFRC users (D3.4)

**Status: not started.**

This deliverable is the last in WP3's dependency chain — a demonstration presupposes a working platform
(D3.3), material to train users on it (D3.1), and, ideally, documentation of how it fits ESA's tooling
(D3.2). No demonstration activity has begun.

## 2.5 Adjacent capabilities already in place

Two pieces of related infrastructure, while not formal WP3 deliverables, materially reduce the risk of
the plan above and are worth noting:

- **Visualisation.** WP2's pipeline design already commits to TiTiler — Development Seed's open-source
  dynamic tiling server — for rendering EO and derived raster layers on the fly. WP3's interactive tools
  reuse this rather than building new visualisation infrastructure, which is a proven, low-risk
  component already operating elsewhere in the Montandon stack.
- **LLM-driven / conversational access.** A separate, already-functioning capability — an MCP
  (Model Context Protocol) service exposing Montandon's event, hazard, and impact data for natural-
  language querying — has been built and deployed, evolved from an earlier Claude-Code-specific skill
  pack into a standard toolset served on Kubernetes. This is not currently scoped as a formal WP3
  sub-deliverable, but it demonstrates a second, complementary "interactive access" pattern alongside
  the Django platform, and is worth folding into the WP3 narrative for the Readiness Review meeting as
  evidence of momentum on the access-patterns side of this work package.
