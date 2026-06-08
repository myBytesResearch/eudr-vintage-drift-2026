# Drift snapshot — 2026-06-08

Canonical published snapshot for the Hansen-vintage drift study
in [`eudr-update-2026`](https://mybytes.com/research/notes/eudr-update-2026).

## Run parameters

- **AOIs**: two 33 × 33 km bounding boxes, centred on Soubré
  (CIV, −6.6033, 5.7833) and Sefwi-Wiawso (GHA, −2.5000, 6.2000).
- **Hansen GFC versions**:
  `UMD/hansen/global_forest_change_2024_v1_12` (loss data through
  2023) and `UMD/hansen/global_forest_change_2025_v1_13`
  (through 2024).
- **Plantation layer**:
  `projects/forestdatapartnership/assets/cocoa/model_2025a`.
- **Threshold τ**: 0.50.
- **Hansen lossyear cut-off**: ≥ 21 (= 2021 calendar year and later).
- **Tree-cover-2000 threshold**: 30 %.
- **Run timestamp**: 2026-06-08T00:00:00Z.

## Files

- `area_summary.csv` — one row per (AOI × Hansen-vintage) with
  plantation area, EUDR-risk area, risk share and full provenance.
- `vintage_drift.csv` — one row per AOI with the 2024-vs-2025
  comparison and the Δ in percentage points (the canonical source
  for Plot 2 of the article).

## Licence pitfall

The Forest Data Partnership cocoa-probability layer is licensed
under **[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)**.
Every risk-share number in `area_summary.csv` and `vintage_drift.csv`
is derived from this NC-licensed layer and **carries the same NC
restriction**:

- Non-commercial use (internal monitoring, research, academic
  publication, blog posts that do not directly monetise these
  numbers): permitted with attribution to FDP.
- Commercial use (paid vendor product, paid report, paid
  compliance service that resells these numbers): **prohibited**
  without a separate sub-licence from the Forest Data
  Partnership.

The code in the repository is MIT-licensed and not affected. The
Hansen-derived loss numbers are also not affected.
