# Use Case 3 - Operational Response Prioritisation

## 3.1 Context and use case relevance

In the first hours and days after a disaster, National Societies and IFRC face a triage problem: with
limited teams, relief items and DREF funds, they must decide **where to act first**. Exposure figures
(Use Case 1) tell them who was at risk before the event, and impact estimates (Use Case 2) tell them
where the disaster hit — but neither, on its own, answers the operational question "which affected
areas should we prioritise in the first 24-72 hours?". Answering it means weighing the **observed
severity** of the event against the **pre-existing vulnerability and coping capacity** of each affected
area, its **history** of disasters and past response, and the **operational reality** of who is already
there and how hard each area is to reach. In the terms of this project's analytics, this is the
resilience-indicators / prioritisation analysis — the third alongside exposure estimation (Use Case 1)
and damage assessment (Use Case 2) — and it synthesises the outputs of both.

Today this prioritisation is largely manual and expert-driven. It is slow, hard to reproduce and
inconsistent between responses, and for the many smaller but frequent disasters there is little
decision support at all. The recent Venezuela earthquake illustrates the gap: following the 24 June
2026 La Guaira earthquake (Copernicus EMS activation EMSR894, GDACS-linked, with UN-SPIDER damage
products), responders faced numerous affected municipalities and had to triage deployment with limited
information on where impact and need concentrated.

This use case delivers a Montandon workflow, coupled with Jupyter notebooks and documentation, that
produces a transparent and adjustable **prioritisation score** and a ranked map and table of affected
administrative units (or areas of interest) for the first days of the response. It combines the
exposure and impact analyses of the two previous use cases with Montandon's historical record and
operational datasets, turning "who is at risk" and "where it hit" into "where to act first".

![Illustrative Montandon response-prioritisation overlay on the Charter Mapper view of activation Act-1036 / EMSR894 (Venezuela earthquake). The nine areas of interest traced by the Charter's authorized users are ranked by a composite priority score (observed impact × vulnerability × historical burden × coverage gap). Scores are synthetic, for demonstration.](figures/charter-mapper-venezuela-prioritised.png)

**Benefit to the International Charter.** The Charter delivers authoritative satellite-derived extent
and damage products, but it carries little humanitarian context and receives little feedback on where
impact and need actually concentrate. This use case gives the Charter a feedback loop. Montandon
combines the Charter's own EO products with exposure, vulnerability, disaster history and operational
coverage to return a prioritisation of areas that helps the On-Duty Operator, Authorized Users and
value-added providers decide which areas to acquire and map next, and helps Charter end-users focus
their reading of the products on the areas that matter most. Value flows both ways: the Charter feeds
observed impact into Montandon, and Montandon returns prioritised humanitarian context to the Charter.

Because it is the use case that closes the loop back to the space-based response ecosystem, it is a
natural conclusion to the series and the most directly relevant to the Charter and to ESA.

## 3.2 Data sources

This use case reuses the data sources of the two previous ones and adds a set of operational datasets.
It relies heavily on Montandon, both as the entry point to the correlated EO and impact data and as the
unique source of harmonised disaster history.

**Montandon Global Crisis Data Bank** - the core source. It provides the current event with its
correlated hazard, impact and EO response products (Copernicus EMS and International Charter activations
and value-added products, carrying the Charter `disaster:` extension), and, uniquely, the historical
events, impacts and past DREF operations for the affected area. This history — how often the area is
hit, how many people were typically affected, what response was mounted — is what lets prioritisation
account for recurrent burden, and it is not readily available from any other single source.

**International Charter / Copernicus Emergency Management Service** - the observed disaster extent and
damage grading, giving the observed severity per area (as in Use Case 2). For the Venezuela example, the
Charter/CEMS activation EMSR894 is both a first-class input to the prioritisation and a consumer of its
output.

**INFORM Subnational Risk Index** - the vulnerability and lack-of-coping-capacity dimensions per
administrative unit (as in Use Case 1), capturing how well each area can absorb and recover from a
shock.

**IFRC GO** - the IFRC's operational platform and the main source of response-side context: National
Society **branch presence** and local capacity, **active emergency operations**, **active DREF
operations**, and related response resources — indicating where response capacity and coverage already
exist, and where they do not. [add link]

**Field reports and assessments** - operational reports and rapid field assessments from responders,
to be surfaced through the planned connection between IFRC's **Emergency Operations Centre (EOC)** and
Montandon. These add on-the-ground observations of needs and access that complement the remote-sensing
and baseline data. *(Planned Montandon connection.)*

**Accessibility and logistics** - road networks, distance to key facilities and known **logistics
constraints** (from OpenStreetMap and operational sources), to flag hard-to-reach or logistically
constrained areas that may need earlier or heavier support.

**Base layers** - population (WorldPop or Global Human Settlement Layer), administrative boundaries
(GADM or Common Operational Datasets) and infrastructure (OpenStreetMap), consistent with Use Cases 1
and 2.

## 3.3 Methodology

The geospatial processing builds on the two previous use cases and combines their outputs into a single,
comparable ranking. For each administrative unit (or custom area of interest) the notebook computes a
set of component signals, each normalised to a common 0-1 scale so they can be combined:

- **Observed severity** - the EO-derived impact and damage grade intersected with the exposed population
  and infrastructure (Use Case 2).
- **Vulnerability and lack of coping capacity** - the corresponding INFORM Subnational dimensions (Use
  Case 1).
- **Historical burden and recurrence** - derived from Montandon's historical events, impacts and DREF
  operations for the area (frequency and magnitude of past events, past response effort).
- **Operational gap and accessibility** (optional) - existing National Society presence and operations
  (from IFRC GO) and remoteness/accessibility, to give weight to affected areas that are under-served or
  hard to reach.

These components are aggregated into a composite **prioritisation index**, using a transparent weighting
scheme (a weighted average, or an INFORM-style geometric mean that prevents a single strong dimension
from dominating). As in the previous use cases, the notebook exposes the key choices to the user: which
components to include, their relative weights, the spatial resolution, the target population or
infrastructure, and the hazard.

**A complementary confidence score.** A ranking is only as reliable as the data behind it, and data
completeness is uneven — some areas are well covered by recent Earth Observation products and rich
historical records, others are not. Alongside the priority score, the workflow therefore computes a
per-area **confidence score** that summarises the completeness and freshness of the underlying data:
the **EO coverage** of the area (whether recent, usable Charter/CEMS products actually cover it), the
**completeness of Montandon's historical record** for the area, and the **age and recency of the
baseline datasets** (population, exposure and vulnerability layers). Presenting priority and confidence
together gives decision-makers a two-axis read: a high-priority area with low confidence is a signal to
verify on the ground — and, for the Charter, a prime candidate for a new acquisition or mapping request.
The analysis thus not only ranks where to act, it also flags where the evidence is weakest and where
additional EO tasking would add the most value.

**A plain-language rationale for every ranking.** The output does not stop at a score or a single
driver. For each area, the notebook also generates a short, automatically-produced **explanation of why
it ranks where it does** — naming the components that pushed it up or down (for example, "high observed
damage combined with repeated historical impacts and high vulnerability", or "moderate impact but poor
accessibility and sparse recent data"). Deriving the rationale directly from the component scores keeps
the ranking **transparent and auditable** rather than a black-box number, and gives responders and
Charter operators the justification alongside the rank.

The result is a ranking and a prioritisation map of the affected areas — a shortlist for the first
24-72 hours — optionally highlighting the areas that combine high observed impact, high vulnerability
and low current coverage as top priorities. For the Venezuela activation, the nine Charter areas of
interest would rank as follows (illustrative — the confidence column reflects data completeness, not
priority):

| Rank | Area of interest | Priority tier | Confidence | Why it ranks here (illustrative) |
| --- | --- | --- | --- | --- |
| 1 | La Guaira | Top | High | Severe observed damage near the epicentre in a dense coastal area, with high vulnerability |
| 2 | Caracas | Top | High | Very large exposed and vulnerable population in the capital, with significant observed impact |
| 3 | El Junquito | High | Medium | High vulnerability and poor access on landslide-prone hillsides amplify a moderate impact |
| 4 | Valencia | High | High | Large urban population exposed, with moderate observed impact and recurrent hazard history |
| 5 | Maracay | High | High | Sizeable urban exposure with moderate observed impact |
| 6 | Turmero | Medium | Medium | Moderate exposure and impact, with few aggravating factors |
| 7 | Morón | Medium | Medium | Coastal exposure with modest observed impact and lower population |
| 8 | San Felipe | Lower | Low | Limited observed impact farther from the strongest shaking, and sparse recent data |
| 9 | Tucacas | Lower | Low | Minimal observed impact and low exposure, with low-confidence data |

An important dimension of this use case is time. A disaster evolves — a flood extent grows, an
earthquake is followed by aftershocks — and so does the prioritisation. As new Copernicus EMS monitoring
products for the same event arrive, the analysis is re-run and the ranking updated, so priorities track
the situation rather than freezing at the first snapshot.

**A natural extension — field observations refining the ranking.** Beyond remote sensing, the same
set-up can absorb **field observations** as they come in. A natural extension, currently being explored
by IFRC and ToggleCorp around the integration of **Emergency Operations Centre (EOC)** data from the
National Societies, would feed responders' own reports and assessments back into Montandon and into this
analysis — progressively sharpening both the **priority** and the **confidence** scores with ground
truth as the response unfolds. This is out of the current scope, but the workflow is deliberately
designed so that such a feed slots in as one more signal, without changing the method.

## 3.4 Integration and delivery to Charter clients

Beyond the notebook, this use case proposes to make the prioritisation directly consumable by client
applications, and in particular by the International Charter's own tools.

The prioritisation output is published as a dedicated Montandon STAC collection (for example a
`response-prioritisation` collection), with one item per ranked area carrying the composite score, its
component values, and links back to the rest of the model: the shared `monty:corr_id` tying it to the
event, a `derived_from` link to the EO response product it is based on, and a `related` link to the
source Charter or CEMS activation.

Exposed through the Montandon STAC API and its queryable fields, this lets a client retrieve, in a
single call, "for Charter activation EMSR894 (or for this event), the ranked priority areas together
with their humanitarian context". Because the collection is correlated to the source activation, the
Charter's own identifier is enough to reach the prioritisation.

This opens two concrete integration paths for Charter users:

- **Charter Mapper** - the prioritisation can be surfaced as an overlay on an activation, so that
  operators and value-added providers see, alongside the EO products, which areas the humanitarian
  analysis flags as highest priority for the next acquisition, mapping and response.
- **A Charter chatbot** - a conversational client over the same API, letting Charter users ask in
  natural language "which areas should be mapped or served first for this activation?" and receive the
  ranked areas with their supporting context.

The actual client integrations are downstream of this use case; what it proposes and demonstrates is the
data product — the prioritisation collection and the API methods — that makes them possible, and that
turns Montandon into an operational decision-support layer for both IFRC responders and the
International Charter.
