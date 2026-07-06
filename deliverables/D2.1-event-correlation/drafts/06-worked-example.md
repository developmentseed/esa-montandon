# End-to-End Worked Example — Spain, October 2024 Floods

To make the correlation of EO products concrete, this section walks through a real disaster. On 27
October 2024, severe flooding struck Spain, principally the Valencia region. Multiple sources recorded
it: **GLIDE** (`FL-2024-000199-ESP`), **GDACS** (event 1102983, several episodes), and **EM-DAT**. ESA
EO services produced mapping products for the same event. The goal is to correlate all of them into one
navigable cluster.

![Copernicus Emergency Management Service monitoring of the October 2024 floods in Valencia, Spain (activation EMSR773) — one of the EO response products correlated to the event below. © European Union, Copernicus Emergency Management Service.](spain-2024-cems.webp)

## Step 1 — Correlate the source events

Find all source events describing the flood (Algorithm 1), across the relevant collections:

```text
'event' IN roles AND
a_contains(monty:country_codes, 'ESP') AND
a_overlaps(monty:hazard_codes, ARRAY['MH0600','nat-hyd-flo-flo','FL']) AND
t_intersects(datetime, INTERVAL('2024-10-27T00:00:00Z','2024-10-28T23:59:59Z'))
```

This returns the GLIDE, GDACS, and EM-DAT events for the flood. One is designated the reference event,
fixing a shared correlation identifier of the form `20241027-ESP-…-FL-…-GCDB` that all related items
will carry.

## Step 2 — Gather hazards and impacts

Using the reference event's `corr_id`, retrieve the associated hazard items (Algorithm 2) and, with a
widened temporal window for reporting lag, the impact items (Algorithm 3): fatalities, people affected,
and economic-loss estimates reported by the various sources.

## Step 3 — Attach the EO response products

As Copernicus EMS and UNOSAT products for the flood are ingested (per D2.1 §5.1), each is anchored on
its source identifier, assigned the event's `corr_id`, and linked to the reference event. Retrieving
every EO product for the disaster is then a single filter:

```text
'response' IN roles AND monty:corr_id = '20241027-ESP-…-FL-…-GCDB'
```

Restricting to delineation and grading products (the flood extent and the damage assessment):

```text
'response' IN roles AND monty:corr_id = '20241027-ESP-…-FL-…-GCDB' AND
monty:response_detail.type IN ('eo-del','eo-gra')
```

## Step 4 — Follow a product to the impacts it informs

The UNOSAT damage-assessment product carries per-thematic figures. Under the boundary rules these are
separate Impact items linked back to the product by `derived_from` and sharing the `corr_id`. From the
product, its downstream impacts are:

```text
monty:corr_id = '20241027-ESP-…-FL-…-GCDB' AND 'impact' IN roles
```

and from any such impact, the source product is recovered by following its `derived_from` link.

## The result

![The correlated cluster for the October 2024 Spain floods: GLIDE, GDACS, and EM-DAT events resolve to one reference event, which links the flood hazard, the impact estimates, and the CEMS and UNOSAT EO response products (with their derived impacts).](spain-cluster.png)

A single correlation identifier now unites, for the October 2024 Spain floods: the GLIDE, GDACS, and
EM-DAT **events**; their **hazard** items; the **impact** estimates; and the ESA/UN **EO response
products** (Copernicus delineation and grading, UNOSAT damage assessment) together with the impact items
those products informed. An IFRC information manager retrieves the entire cluster — humanitarian and
Earth Observation data side by side — with a single query, without needing to know that the data
originated from six different organisations. This is the operational payoff of adapting the correlation
system to EO products.
