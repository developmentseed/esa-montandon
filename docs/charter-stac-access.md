# Charter STAC Catalog Access

## Base URL
```
https://supervisor.disasterscharter.org/api
```

## IP Allowlist
- `178.105.74.184` - DevSeed dev server (Hetzner)
- `110.34.1.108` (Toggle Testing)
- `20.223.144.10` - IFRC staging cluster
- `137.135.138.134` - IFRC production cluster

## Endpoints

**Calls**
- Catalog: `/calls` (slow, dynamically generated)
- Item: `/calls/{callId}`

**Activations**
- Catalog: `/activations` (broken item links)
- Item: `/activations/act-{activationId}` (use this pattern directly)

**Areas**
- From activation items via `related` links
- Example: `/activations/act-1019/areas/Juiz_de_Fora-QVwJEJDB0IZNzAO3SVGtOw__.json`

## Data Model
```
Call → Activation → Area → Acquisition → Dataset → Value Added Product
```

## Contact
Zachary Foltz (ACRI-ST): zachary.foltz@acri-st.fr
