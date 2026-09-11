# State of Work

## 2.1 Notebook-publishing pipeline (D3.3 core)

**Status: four core pieces identified; notebook generation and static-site compilation are already
running in production; triggering and distribution are not yet built.**

An earlier draft of this report proposed a specific architecture: a Django orchestration app, a Celery
job queue, and Kubernetes execution. That level of commitment is more than this checkpoint needs, as other architectural setups exist (with tradeoffs that will need to be assessed). This
report instead identifies the pipeline's core functional pieces and assesses confidence in each
individually (Section 3), leaving the specific orchestration technology as an implementation choice
rather than a fixed design decision at this stage, based on functionality requests and capacity constraints. The four pieces, in the order a run passes through
them, are:

1. **Triggers** — what starts a run: a WP2 automated event (for example, a flood-event threshold being
   met), a user's manual parameter selection, or a scheduled job.
2. **Notebook generation** — parameter extraction and a papermill run of the chosen notebook template,
   producing a parameterised notebook output.
3. **Static site compilation** — a MyST/Jupyter Book build of the notebook output into static HTML.
4. **Access and distribution** — a hosted, permanent URL, plus onward distribution such as email
   notification and integration into external platforms (Montandon, IFRC's GO platform, etc.),

**Notebook generation and static site compilation are already running in production**, via WP2's Use
Case 1: its data-preparation, exposure-calculation, and visualization notebooks take a country parameter
and run end to end via papermill, validated for more than one country, and the output is published to a
live MyST site (D2.3, Section 2.1). This proves the platform's central mechanism, pieces 2 and 3 above,
well ahead of building anything else around it. An earlier Streamlit prototype explored a guided-form
interface for the same use case but is not expected to carry forward.

**Triggers and access/distribution are not yet built.** The automated-event trigger is proven, reused
directly from WP2's pipeline (D2.2); manual and scheduled triggering are not, and need a backing service that proposal's specifics
remain reasonable direction but are not a locked-in decision. On the distribution side, a live URL for a
published static site already exists for Use Case 1. Email notification and internal and external-platform
integrations are ideated but not concrete yet.

Of the three use cases (risk exposure, impact estimation, response prioritization; see D2.z3), Use Case 1
and Use Case 2 are already built and would run through the notebook-generation and static-site pieces as
templates once a trigger exists; Use Case 3 will follow once built. Per D2.3's Section 2.3, its
near-term activity is now an externally-led Utility Report rather than a build, so it has no near-term
template to register here.

**What remains.** Designing and building the trigger/orchestration piece, and generalizing static-site
compilation and distribution beyond the single Use Case 1 path. Four specific design questions remain
open (Section 4) and should be resolved before committing to an implementation for the trigger
piece, since they affect its data model and compute strategy.

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

- **Visualisation.** WP3's interactive tools build on `manywidgets`, a Development Seed library built
  from the open-source `anywidget` project, for rendering EO and derived layers interactively within
  notebooks. This is a component already operating elsewhere in the Montandon stack,
  reused here rather than building new visualisation infrastructure from scratch.
- **LLM-driven / conversational access.** A separate, already-functioning capability, an MCP (Model
  Context Protocol) service exposing Montandon's event, hazard, and impact data for natural-language
  querying, has been built and deployed, evolved from an earlier Claude-Code-specific skill pack into a
  standard toolset served on Kubernetes. This is not currently scoped as a formal WP3 sub-deliverable,
  but it demonstrates a second, complementary "interactive access" pattern alongside the
  notebook-publishing pipeline, and is worth including in the WP3 narrative for the Readiness Review
  meeting as evidence of momentum on the access-patterns side of this work package.
