# STAC Extension Interoperability (Layering)

A key interoperability decision is that Monty Response items **declare multiple STAC extensions and
reuse their fields** rather than duplicating every concept under the `monty:` prefix. This
"extension layering over duplication" principle is what lets a Montandon Response item remain
interoperable with the wider EO tooling ecosystem — a client that understands the Terradue `disaster:`
or the `processing:` extension can read those fields directly. The rules are published as the Monty
**Response Best Practices** document accompanying v1.3.0.

## Governing principles

1. **Extension layering over duplication.** Where a third-party STAC extension covers a concept
   (Terradue `disaster:` for Charter items, `processing:` for derived EO products, `eo:` / `sar:` /
   `sat:` for source imagery), the Response item declares that extension and uses its fields directly.
2. **Acquisition vs. Response layer separation.** The `sat:`, `eo:`, `sar:`, and `view:` extensions
   describe the *source imagery* a product is derived from. They apply to the acquisition items reached
   via `derived_from`, not to the derived Response product — with one exception (`eo-dat`, where the
   deliverable *is* the imagery dataset).
3. **`monty:` is always declared**, carrying at least `response_detail.type`, `corr_id`,
   `country_codes`, `hazard_codes`, and the `response` role.
4. **`monty:response_detail` is the residual carrier** — it holds the type code and Monty-specific
   metadata not already expressed by another declared extension.
5. **Statistical figures go to Impact items** (Section 6).

## Extension stack per source

| Response source | Extensions declared on the Response item |
| --- | --- |
| CEMS Rapid Mapping (`eo-ref` … `eo-vap`) | `monty:` + `processing:` (recommended) |
| International Charter VAP (`eo-del`, `eo-gra`, `eo-vap`, …) | `monty:` + `disaster:` (**mandatory**) + `processing:` |
| UNOSAT (`eo-fep`, `eo-del`, `eo-gra`, …) | `monty:` + `processing:` (recommended) |
| Charter delivered acquisition (`eo-dat`) | `monty:` + `disaster:` + `eo:` / `sar:` / `sat:` (the item *is* the imagery) |
| Humanitarian (`hum-*`) | `monty:` only |

![Extension layering per source. Every Response item declares `monty:`; Charter VAPs additionally declare the Terradue `disaster:` extension; source imagery is described by `eo:`/`sar:`/`sat:` on the linked acquisition item, reached via `derived_from`.](extension-layering.png)

No CEMS or UNOSAT STAC extension exists, so their source-specific fields (product status, monitoring
iteration) are carried under `monty:response_detail`. For the Charter, the `disaster:` extension is
declared and its fields (`disaster:class`, `disaster:activation_id`, `disaster:activation_status`,
`disaster:resolution_class`, `disaster:types`) are used as-is and **must not** be duplicated in
`response_detail`.

## Worked example — Charter Value-Added Product

A Charter delineation VAP declares both `monty:` and `disaster:`; the Charter-native fields live in
`disaster:`, and only the Monty-specific residue lives in `response_detail`:

```json
{
  "stac_extensions": [
    "https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json",
    "https://terradue.github.io/stac-extensions-disaster/v1.1.0/schema.json"
  ],
  "properties": {
    "disaster:class": "vap",
    "disaster:activation_id": 849,
    "disaster:activation_status": "open",
    "disaster:resolution_class": "VHR",
    "disaster:types": ["flood"],
    "monty:response_detail": {
      "type": "eo-vap",
      "source_id": "ACT-849",
      "producer": "Airbus",
      "methodology": "human_interpreted",
      "sendai_targets": ["D", "G"]
    }
  }
}
```

Note the absence of `status` and `resolution_class` under `response_detail` — they are carried by the
`disaster:` extension on the same item.

## Anti-patterns avoided

The best-practices document explicitly forbids: duplicating `disaster:` fields under `response_detail`;
carrying `sar:`/`eo:`/`sat:` fields on a *derived* product item (they belong on the linked acquisition);
stuffing damage statistics into `response_detail` (they become Impact items); mixing the source into
the type code (`eo-cems-del` — use source-agnostic `eo-del`); and creating multiple codes for
monitoring iterations (use `monitoring_number`).
