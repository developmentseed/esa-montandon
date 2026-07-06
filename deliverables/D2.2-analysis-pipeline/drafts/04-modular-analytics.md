# Modular Analytics Workflow Model

The analytical content of the pipeline is organised as a suite of **modular notebooks**. This section
describes the model at architecture level; the specific algorithms are developed during WP2 execution.

## Notebooks as interchangeable objects

Each analysis is a Jupyter notebook that is:

- **Parameterised** — it takes the country, the event (via its correlation identifier), and the relevant
  data references as parameters, and is executed for a specific event by injecting those parameters
  (using papermill). One notebook template therefore serves every event of its kind.
- **Contract-bound** — it declares defined inputs and outputs. Because two notebooks with the same input
  and output contract are interchangeable, a method can be replaced by a better one, or specialised for a
  region, without changing anything around it.
- **Self-documenting** — the methodology, its scientific basis, and its limitations are documented in the
  notebook itself, so the analysis and its explanation travel together.

Treating notebooks as objects in a workflow — substitutable provided inputs and outputs match — is what
makes the pipeline extensible and supports experimentation: analysts develop and refine methods in
notebooks, and the pipeline runs whichever notebook is registered for a given hazard and analysis type.

## The analysis families

Three families of analysis are provided, each addressing an operational priority. They are named here at
architecture level; the detailed methods are a WP2 execution activity, reviewed with IFRC and prioritising
peer-reviewed, openly accessible algorithms.

| Analysis family | Question it answers | Typical EO input |
| --- | --- | --- |
| **Exposure estimation** | How many people / how much infrastructure lies within the observed hazard extent? | Flood extent, burned area, hazard footprint |
| **Damage assessment** | What is damaged, and to what degree, in the affected area? | Grading products, damage layers (Copernicus, UNOSAT) |
| **Resilience indicators / response prioritisation** | Which affected areas should be prioritised for response, combining exposure, impact, vulnerability, history and coverage? | Synthesises the exposure and damage outputs above |

These three families correspond directly to the use cases detailed in deliverable **D2.4**: exposure
estimation (Use Case 1), damage / impact assessment (Use Case 2), and resilience-based response
prioritisation (Use Case 3, which synthesises the other two). They map onto the WP2 operational
priorities and the hazard types prioritised for the activity (floods, wildfires, earthquakes, and
cyclones). Beyond a value or a score, an analysis output can carry a **data-completeness confidence
measure** and an automatically generated **plain-language rationale**, so results are transparent and
auditable rather than opaque numbers.

![A Copernicus EMS grading product (per-feature damage classification, EMSR773 Valencia) — an example of the EO damage layer the damage-assessment notebook family consumes. © European Union, Copernicus Emergency Management Service.](cems-gra-example.png)

## Notebook catalog and substitution

The notebooks live in a version-controlled repository (the analysis-code repository in the architecture)
and are referenced by the orchestration through the analysis matrix (Section 6). Adding a capability —
a new hazard type, a refined method, a region-specific variant — means committing a notebook that
honours the input/output contract and registering it in the matrix. No pipeline code changes. This is
the mechanism that keeps the system maintainable and lets IFRC and its partners sustain and extend it
beyond the project.

## Relationship to WP3

The same notebooks are the foundation for the Work Package 3 interactive tools and training: the
methods developed as pipeline notebooks are also the artifacts that National Society users learn to run
and adapt, and the visualisation components (including dynamic tiling via TiTiler) reuse the same
outputs. The modular model therefore serves both the automated pipeline and the human-facing tools.
