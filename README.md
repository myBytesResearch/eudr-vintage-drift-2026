# `eudr-vintage-drift-2026`

> **Status:** Companion repository for the myBytes article
> [`Sechs Monate vor dem neuen EUDR-Stichtag`](https://mybytes.com/research/eudr-update-2026).
> Self-contained reproducibility bundle for the Hansen-vintage
> drift comparison published in §2 of the article. Private during
> the editorial-cool-down phase, planned visibility flip to public
> on publication.

## What this repo proves

The article claims that between Hansen Global Forest Change
vintage `v2024_v1_12` (forest-loss data through 2023) and vintage
`v2025_v1_13` (through 2024) the EUDR-risk share on the same
33 × 33 km cocoa-belt AOIs **drifts measurably upward**, even
though the EU postponed the regulation's effective date.

Concrete numbers, all reproducible from this repo:

| AOI | 2024 vintage | 2025 vintage | Δ |
|---|---|---|---|
| Soubré, CIV (33 × 33 km) | 2.28 % | 2.74 % | +0.45 pp |
| Sefwi-Wiawso, GHA (33 × 33 km) | 5.13 % | 6.05 % | +0.93 pp |

## How to reproduce

```
git clone git@github.mybytes-com:myBytesResearch/eudr-vintage-drift-2026.git
cd eudr-vintage-drift-2026
pip install -r requirements.txt
jupyter notebook notebooks/00_reproduce_drift_numbers.ipynb
```

The notebook loads `data/runs/2026-06-08/vintage_drift.csv` (the
canonical published snapshot) and asserts the four numbers above
with a tolerance of ± 0.05 percentage points. If the assertion
passes, the article numbers reproduce. If it fails, the snapshot
and the article have drifted apart — that is a publishability
gate.

## How the numbers were computed

The drift run lives in `scripts/build_snapshot_2026_06_08.py`.
It runs against Google Earth Engine and needs a registered GEE
project. For each (AOI × Hansen-vintage) combination it computes

```
plantation_ha  = sum of pixelArea where FDP_prob   >= τ
risk_ha        = sum of pixelArea where MaskA AND MaskB
risk_share_pct = 100 * risk_ha / plantation_ha
```

with

- **τ = 0.50** on the Forest Data Partnership cocoa probability
- **treecover2000 ≥ 30 %** on Hansen
- **lossyear ≥ 21** (= calendar year 2021 and later)

The reusable mask + operation code under `src/` is the
methodologically authoritative implementation, kept in sync
with the companion methodology repo
[`eudr-risk-pipeline`](https://github.com/myBytesResearch/eudr-risk-pipeline).
For the full method and its rationale see that repo; this one
focuses on the **vintage-drift study only**.

## Repository contents

```
.
├── README.md                         ← you are here
├── LICENSE                           ← MIT (code) + CC BY 4.0 (content)
├── requirements.txt
├── data/
│   └── runs/2026-06-08/              ← canonical published snapshot
│       ├── area_summary.csv          ← (AOI × vintage) area + risk values
│       └── vintage_drift.csv         ← drift table reproduced in Plot 2
├── notebooks/
│   └── 00_reproduce_drift_numbers.ipynb
├── scripts/
│   └── build_snapshot_2026_06_08.py  ← live GEE build (needs GEE access)
├── src/
│   ├── aois.py                       ← AOI registry (33 km town-centred)
│   ├── masks/                        ← Hansen + plantation mask builders
│   ├── operations/eudr_risk.py       ← the AND operation
│   └── io/snapshots.py               ← snapshot loaders
└── docs/methodology.md
```

## Data sources

| Layer | GEE asset | Resolution | Licence |
|---|---|---|---|
| Forest loss, 2024 vintage | `UMD/hansen/global_forest_change_2024_v1_12` | 30 m | open, attribution. Commercial reuse OK. |
| Forest loss, 2025 vintage | `UMD/hansen/global_forest_change_2025_v1_13` | 30 m | open, attribution. Commercial reuse OK. |
| Cocoa plantation probability | `projects/forestdatapartnership/assets/cocoa/model_2025a` | 10 m | **[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial** |

### License pitfall — read before commercial use

The cocoa-plantation-probability layer is licensed under
**CC BY-NC 4.0**. Concretely:

- You **may** reproduce the drift methodology with your own input
  data for **internal use, research or non-commercial publication**
  with attribution to FDP.
- You **may not** publish, redistribute or sell the derived
  numerical values (2.28 / 2.74 / 5.13 / 6.05 %) **commercially**
  without a separate licensing agreement with the Forest Data
  Partnership.
- The **code** in this repository, the AOI registry, the Hansen-
  derived loss numbers and the documentation are **not** affected
  by the NC clause and can be used commercially under MIT.

## Licence

Three distinct licences apply:

- **Code** (everything under `src/`, `notebooks/`, `scripts/`):
  [MIT](LICENSE). Commercial reuse allowed with attribution.
- **Documentation, README, AOI definitions**:
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- **FDP-derived numerical values** (every risk-share value in
  this repository):
  **[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)** —
  upstream Forest Data Partnership. Commercial redistribution
  prohibited without FDP sub-licence.

## Citation

```
Winger, G. (2026). eudr-vintage-drift-2026 — Hansen-vintage
drift snapshot for EUDR-risk monitoring in the West-African
cocoa belt. Snapshot 2026-06-08. myBytesResearch.
```

## Issues, PRs, criticism

The repository is open for critique. Especially welcome: ground-
truth validation of the drift signal, threshold-sensitivity
analyses on τ, equivalent drift studies on other commodities.
