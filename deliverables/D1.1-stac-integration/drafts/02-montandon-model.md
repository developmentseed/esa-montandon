# The Montandon Data Model and the Response Gap

## The four-construct model

Montandon organises disaster data around four item types, each represented as a STAC Item and linked
through a shared correlation identifier and explicit STAC relation links:

- **Event** — a disaster event that has occurred or is forecast, carrying date, time, and location, and
  referencing the hazards that affect it. Every source produces at least an Event item; it provides the
  context that anchors all other items.
- **Hazard** — a process, phenomenon, or human activity that may cause harm, carrying a hazard code
  from a recognised classification system plus severity or magnitude.
- **Impact** — an estimated effect of a hazard, such as the number of fatalities, people affected,
  buildings destroyed, or economic loss.
- **Response** — an action taken or a product produced in response to a disaster.

![The four-construct Monty model. Response is the construct completed by this activity; its `monty:response_detail` object carries the response type and metadata, and it links to the Event, Hazard, and Impact items that describe the same disaster.](monty-class-model.png)

Events, Hazards, and Impacts were fully specified and operational before this activity, with data
flowing from sources such as GDACS, EM-DAT, DesInventar, USGS, GLIDE, IDMC, PDC, and the IFRC DREF
system. Each item declares the **Monty STAC extension** (`monty:`), which adds the fields — hazard
codes, country codes, correlation identifier, and the `hazard_detail` / `impact_detail` objects — that
make heterogeneous source data queryable through one interface.

## The gap: an undefined Response construct

Of the four constructs, **Response was the only one not implemented**. In the original Montandon
schema it contained a single `ID_linkage` field: no taxonomy of response types, no descriptive fields,
and no STAC representation. In practice this meant Montandon could record *what happened* (Event,
Hazard) and *who and what was affected* (Impact), but not *what was done in response* — the mapping
activations, delineation maps, damage assessments, and value-added products that EO services generate
during a crisis.

This gap is precisely where ESA's EO ecosystem provides the missing dimension. A Charter activation,
a Copernicus EMS rapid-mapping product, or a UNOSAT damage assessment is a concrete manifestation of a
response activity. Making these first-class citizens of the Montandon model is the central data-modelling
task of WP1, and completing the Response construct is what allows ESA EO products to be catalogued,
discovered, and linked to the events and impacts they document.

## Platform foundation

Montandon is built on Development Seed's open-source **eoAPI** framework. It exposes a **STAC API** with
the OGC-aligned Filter (CQL2) extension for querying, dynamic tiling for raster visualisation, and
automated ETL pipelines that harmonise fragmented sources. The staging deployment is reachable at
`https://montandon-eoapi-stage.ifrc.org/stac`. Because the platform is STAC-native and API-driven, the
work of integrating EO products is fundamentally a **data-modelling and mapping** exercise: define how
each EO product is represented as a Monty Response item, and the existing infrastructure makes it
discoverable and queryable alongside all other Montandon data.

The remainder of this report describes how the Response construct was designed, how it reuses existing
EO and disaster STAC standards, and how each priority EO source maps onto it.
