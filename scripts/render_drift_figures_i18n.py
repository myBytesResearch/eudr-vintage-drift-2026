"""Localized (DE/EN/PL) render of plot2_vintage_drift for 3A1-02.

Computes the Hansen-vintage drift ONCE via GEE (reduceRegion over two AOIs ×
two vintages), then renders the bar chart per language. Needs Google Earth Engine.

DE = plot2_vintage_drift.png canonical, EN/PL = plot2_vintage_drift.<loc>.png.
PL draft -> Mariusz. Numbers identical across languages.
"""

from __future__ import annotations

from pathlib import Path

import ee
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path(__file__).resolve().parents[1] / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

ee.Initialize(project="mybytes-research-2026")

AOIS = {"Soubré, CIV": (-6.6033, 5.7833), "Sefwi-Wiawso, GHA": (-2.5000, 6.2000)}
HALF_KM = 33.0 / 2
TAU = 0.50
VINTAGE_ASSETS = {
    "v2024": "UMD/hansen/global_forest_change_2024_v1_12",
    "v2025": "UMD/hansen/global_forest_change_2025_v1_13",
}
VINTAGE_IDS = ["v2024", "v2025"]


def bbox(lon: float, lat: float) -> ee.Geometry:
    dlon = HALF_KM / (111.0 * np.cos(np.deg2rad(lat)))
    dlat = HALF_KM / 111.0
    return ee.Geometry.Rectangle([lon - dlon, lat - dlat, lon + dlon, lat + dlat])


def fdp_image() -> ee.Image:
    coll = ee.ImageCollection("projects/forestdatapartnership/assets/cocoa/model_2025a")
    img = ee.Image(coll.sort("system:time_start", False).first())
    bands = img.bandNames().getInfo()
    band = next((b for b in bands if "prob" in b.lower() or "cocoa" in b.lower()), bands[0])
    return img.select(band)


print("Loading FDP layer ...")
fdp = fdp_image()
mask_b = fdp.gte(TAU)
pixel_area = ee.Image.pixelArea()


def reduce_ha(image: ee.Image, region: ee.Geometry) -> float:
    masked_area = pixel_area.updateMask(image)
    res = masked_area.reduceRegion(reducer=ee.Reducer.sum(), geometry=region,
                                   scale=30, maxPixels=1e10, bestEffort=True)
    return res.get("area").getInfo() / 10_000.0


results: dict[tuple[str, str], float] = {}
for aoi_name, (lon, lat) in AOIS.items():
    region = bbox(lon, lat)
    plant_ha = reduce_ha(mask_b, region)
    print(f"{aoi_name}: plantation_ha = {plant_ha:,.0f}")
    for vid in VINTAGE_IDS:
        h = ee.Image(VINTAGE_ASSETS[vid])
        ma = h.select("treecover2000").gte(30).And(h.select("lossyear").gte(21))
        risk_ha = reduce_ha(ma.And(mask_b), region)
        results[(aoi_name, vid)] = 100 * risk_ha / plant_ha if plant_ha else float("nan")
        print(f"  {vid}: share = {results[(aoi_name, vid)]:.2f} %")

TITLE_COLOR, SUBTLE = "#1a1a1a", "#666666"
COLOR_2024, COLOR_2025 = "#A6B5C2", "#003B71"

LOCALES: dict[str, dict] = {
    "de": {
        "dec": ",", "vint": {"v2024": "Hansen 2024 (Loss bis 2023)", "v2025": "Hansen 2025 (Loss bis 2024)"},
        "ylabel": "EUDR-Risiko-Anteil  ·  Prozent der Plantagen-Fläche",
        "suptitle": "Das Monitoring zählt weiter, während Brüssel den Stichtag verschiebt",
        "subtitle": "Hansen-Vintage-Vergleich für zwei Cocoa-Belt-AOIs. Die Verschiebung am EU-Stichtag ändert die Anbau-Realität nicht.",
        "src": "Quellen: Hansen GFC v2024_v1_12 + v2025_v1_13 (UMD);  FDP Cocoa Probability 2025a (τ = 0,50);  AOI je 33 × 33 km um Soubré (CIV) und Sefwi-Wiawso (GHA).  myBytes Satelliten-Monitoring, abgerufen 2026-06-08.",
    },
    "en": {
        "dec": ".", "vint": {"v2024": "Hansen 2024 (loss through 2023)", "v2025": "Hansen 2025 (loss through 2024)"},
        "ylabel": "EUDR risk share  ·  percent of plantation area",
        "suptitle": "The monitoring keeps counting while Brussels postpones the deadline",
        "subtitle": "Hansen vintage comparison for two cocoa-belt AOIs. Postponing the EU deadline does not change the cultivation reality.",
        "src": "Sources: Hansen GFC v2024_v1_12 + v2025_v1_13 (UMD);  FDP Cocoa Probability 2025a (τ = 0.50);  AOI each 33 × 33 km around Soubré (CIV) and Sefwi-Wiawso (GHA).  myBytes satellite monitoring, retrieved 2026-06-08.",
    },
    "pl": {
        "dec": ",", "vint": {"v2024": "Hansen 2024 (utrata do 2023)", "v2025": "Hansen 2025 (utrata do 2024)"},
        "ylabel": "Udział ryzyka EUDR  ·  procent powierzchni plantacji",
        "suptitle": "Monitoring liczy dalej, podczas gdy Bruksela przesuwa termin",
        "subtitle": "Porównanie wersji Hansen dla dwóch AOI w pasie kakaowym. Przesunięcie unijnego terminu nie zmienia realiów upraw.",
        "src": "Źródła: Hansen GFC v2024_v1_12 + v2025_v1_13 (UMD);  FDP Cocoa Probability 2025a (τ = 0,50);  AOI po 33 × 33 km wokół Soubré (CIV) i Sefwi-Wiawso (GHA).  myBytes monitoring satelitarny, pobrano 2026-06-08.",
    },
}


def fmt(v: float, dec: str) -> str:
    return f"{v:.2f}".replace(".", dec)


def render(loc: str, L: dict) -> None:
    aoi_labels = list(AOIS.keys())
    n = len(aoi_labels)
    x = np.arange(n)
    width = 0.36
    s24 = [results[(a, "v2024")] for a in aoi_labels]
    s25 = [results[(a, "v2025")] for a in aoi_labels]

    fig, ax = plt.subplots(figsize=(12, 5.6), dpi=160)
    fig.patch.set_facecolor("white")
    ax.bar(x - width / 2, s24, width, color=COLOR_2024, label=L["vint"]["v2024"])
    ax.bar(x + width / 2, s25, width, color=COLOR_2025, label=L["vint"]["v2025"])
    for i, (a, b) in enumerate(zip(s24, s25)):
        ax.text(i - width / 2, a + 0.15, f"{fmt(a, L['dec'])} %", ha="center", va="bottom",
                fontsize=10, color=TITLE_COLOR, fontweight="bold")
        ax.text(i + width / 2, b + 0.15, f"{fmt(b, L['dec'])} %", ha="center", va="bottom",
                fontsize=10, color=TITLE_COLOR, fontweight="bold")
        delta = b - a
        sign = "+" if delta >= 0 else ""
        ax.annotate(f"Δ {sign}{fmt(delta, L['dec'])} pp", xy=(i, max(a, b) + 0.85),
                    ha="center", va="bottom", fontsize=10.5, color="#C62828", fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(aoi_labels, fontsize=11, fontweight="bold")
    ax.set_ylabel(L["ylabel"], fontsize=10, color=SUBTLE)
    ax.set_ylim(0, max(s25) * 1.25 + 1)
    ax.tick_params(axis="y", colors=SUBTLE, labelsize=9)
    ax.tick_params(axis="x", length=0)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#cccccc")
    ax.spines["bottom"].set_color("#cccccc")
    ax.grid(axis="y", color="#eeeeee", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2, frameon=False, fontsize=10)
    fig.suptitle(L["suptitle"], x=0.02, y=0.965, ha="left", fontsize=15, fontweight="bold", color=TITLE_COLOR)
    fig.text(0.02, 0.905, L["subtitle"], fontsize=10, color=SUBTLE)
    fig.text(0.02, 0.02, L["src"], fontsize=8, color=SUBTLE)
    fig.subplots_adjust(left=0.07, right=0.97, top=0.80, bottom=0.26)
    suffix = "" if loc == "de" else f".{loc}"
    fig.savefig(OUT_DIR / f"plot2_vintage_drift{suffix}.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    for loc, L in LOCALES.items():
        render(loc, L)
    print(f"Rendered DE/EN/PL vintage_drift to {OUT_DIR}")
    for p in sorted(OUT_DIR.glob("plot2_vintage_drift*.png")):
        print(f"  {p.name} ({p.stat().st_size / 1024:.1f} KB)")
