"""Localized (EN/PL) renders of the localizable 3A1-02 (eudr-update) plots.

Covers plot1_regulatory_timeline and plot3_roadmap_quarters. plot2_vintage_drift
is NOT covered: it needs a live Google Earth Engine call (two Hansen vintages on
one AOI) and cannot run in the sandbox.

PL labels are a first draft for Mariusz review. Numbers/dates are unchanged.

Output: ~/myBytes-workplace/articles/eudr-update-2026/figures/plot{1,3}_*.<loc>.png
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src" / "common"))

from executive_plots import (  # noqa: E402
    RoadmapAction,
    TimelineEvent,
    executive_regulatory_timeline,
    executive_roadmap_quarters,
    set_source_prefix,
)

OUT_DIR = Path(__file__).resolve().parents[1] / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

QUARTERS = ["Q3 2026", "Q4 2026", "Q1 2027", "Q2 2027"]
# priority of each action, by quarter — language-invariant
PRIORITIES = [
    ["mandatory", "mandatory", "recommended"],
    ["mandatory", "mandatory", "recommended", "mandatory"],
    ["recommended", "recommended", "strategic"],
    ["mandatory", "strategic", "mandatory"],
]

LOCALES: dict[str, dict] = {
    "en": {
        "source_prefix": "Source: ",
        "events": [
            ("2023-06-09", "Reg. 2023/1115\nin Official Journal\n09.06.2023", "original"),
            ("2024-12-30", "Original deadline\nlarge operators\n30.12.2024", "original"),
            ("2024-12-19", "First\npostponement\n19.12.2024", "revised"),
            ("2025-12-18", "Second postponement\n+ simplifications\n18.12.2025", "revised"),
            ("2026-12-30", "New deadline\nlarge operators\n30.12.2026", "revised"),
            ("2027-06-30", "New deadline\nSMEs\n30.06.2027", "revised"),
        ],
        "track_labels": {
            "original": "Original (Reg. 2023/1115, June 2023)",
            "revised": "After two postponements + Omnibus 2026",
        },
        "timeline_title": "Two EUDR deadline sets, the same cultivation realities on the ground",
        "timeline_caption": ("Three regulatory interventions in 18 months. The findings from our "
                             "satellite monitoring in the cocoa belt change independently of them."),
        "timeline_source": ("EU Official Journal L 150/206 (2023-06-09), EU Council press release "
                            "2025-12-18, EU Parliament 2025-12-17, Official Journal EU 2026/470 (2026-02-26)"),
        "timeline_xlabel": "Calendar year",
        "priority_labels": {"mandatory": "Mandatory", "recommended": "Recommended", "strategic": "Strategic"},
        "actions": [
            ["Inventory of operators placing on the market in your own EUDR-relevant supply chain",
             "Methodological audit of the compliance providers in use",
             "Check the threshold sensitivity of the provider methodology"],
            ["Obtain and validate geo-polygons of all suppliers",
             "Assess risk concentration on individual operators",
             "Anchor compliance clauses in 2027 contract renewals",
             "Deadline 30.12.2026: large operators subject to application"],
            ["Monitor enforcement cases of the EU Commission",
             "Monitor price premiums on increasingly scarce EUDR-compliant goods",
             "Transfer the methodology to further EUDR commodities (e.g. soy)"],
            ["Onboard SME suppliers into the due-diligence process",
             "Implement the methodology for further EUDR commodities (e.g. palm oil)",
             "Deadline 30.06.2027: SMEs subject to application"],
        ],
        "roadmap_title": "What buyers of an EUDR-relevant commodity should check between today and the SME deadline",
        "roadmap_caption": ("Four quarters, three priority levels. Mandatory actions are deadline-bound; "
                            "strategic ones extend the methodology to further commodities."),
        "roadmap_source": ("Own compilation from EUDR Art. 9, Art. 10 and Art. 24 as well as the Omnibus "
                           "revision 2025/2026. Generic assessment grid, not product- or provider-specific."),
    },
    "pl": {
        "source_prefix": "Źródło: ",
        "events": [
            ("2023-06-09", "Rozp. 2023/1115\nw Dzienniku Urz.\n09.06.2023", "original"),
            ("2024-12-30", "Pierwotny termin\nduże podmioty\n30.12.2024", "original"),
            ("2024-12-19", "Pierwsze\nprzesunięcie\n19.12.2024", "revised"),
            ("2025-12-18", "Drugie przesunięcie\n+ uproszczenia\n18.12.2025", "revised"),
            ("2026-12-30", "Nowy termin\nduże podmioty\n30.12.2026", "revised"),
            ("2027-06-30", "Nowy termin\nMŚP\n30.06.2027", "revised"),
        ],
        "track_labels": {
            "original": "Pierwotnie (Rozp. 2023/1115, czerwiec 2023)",
            "revised": "Po dwóch przesunięciach + Omnibus 2026",
        },
        "timeline_title": "Dwa zestawy terminów EUDR, te same realia upraw w terenie",
        "timeline_caption": ("Trzy interwencje regulacyjne w 18 miesięcy. Wyniki naszego monitoringu "
                             "satelitarnego w pasie kakaowym zmieniają się od nich niezależnie."),
        "timeline_source": ("Dziennik Urzędowy UE L 150/206 (2023-06-09), komunikat Rady UE 2025-12-18, "
                            "Parlament Europejski 2025-12-17, Dziennik Urzędowy UE 2026/470 (2026-02-26)"),
        "timeline_xlabel": "Rok kalendarzowy",
        "priority_labels": {"mandatory": "Obowiązkowe", "recommended": "Zalecane", "strategic": "Strategiczne"},
        "actions": [
            ["Inwentaryzacja podmiotów wprowadzających do obrotu we własnym łańcuchu dostaw objętym EUDR",
             "Audyt metodyczny stosowanych dostawców rozwiązań compliance",
             "Sprawdzić wrażliwość progową metodyki dostawcy"],
            ["Pozyskać i zweryfikować geo-poligony wszystkich dostawców",
             "Oszacować koncentrację ryzyka na poszczególnych podmiotach",
             "Zakotwiczyć klauzule compliance w przedłużeniach umów na 2027",
             "Termin 30.12.2026: duże podmioty objęte obowiązkiem"],
            ["Obserwować przypadki sankcji Komisji Europejskiej",
             "Obserwować premie cenowe na coraz rzadszy towar zgodny z EUDR",
             "Przenieść metodykę na kolejne towary EUDR (np. soja)"],
            ["Wdrożyć dostawców MŚP do procesu due diligence",
             "Wdrożyć metodykę dla kolejnych towarów EUDR (np. olej palmowy)",
             "Termin 30.06.2027: MŚP objęte obowiązkiem"],
        ],
        "roadmap_title": "Co nabywcy towaru objętego EUDR powinni sprawdzić między dziś a terminem dla MŚP",
        "roadmap_caption": ("Cztery kwartały, trzy poziomy priorytetu. Działania obowiązkowe są związane "
                            "z terminami, strategiczne rozszerzają metodykę na kolejne towary."),
        "roadmap_source": ("Własne zestawienie z EUDR art. 9, art. 10 i art. 24 oraz rewizji Omnibus "
                           "2025/2026. Generyczny schemat oceny, nie specyficzny dla produktu ani dostawcy."),
    },
}


def render_locale(loc: str, L: dict) -> None:
    set_source_prefix(L["source_prefix"])

    events = [TimelineEvent(d, lbl, trk) for d, lbl, trk in L["events"]]
    fig1, _ = executive_regulatory_timeline(
        events,
        tracks=["original", "revised"],
        track_labels=L["track_labels"],
        title=L["timeline_title"],
        caption=L["timeline_caption"],
        source=L["timeline_source"],
        x_axis_label=L["timeline_xlabel"],
    )
    fig1.savefig(OUT_DIR / f"plot1_regulatory_timeline.{loc}.png", dpi=160, bbox_inches="tight")

    actions = [[RoadmapAction(text, prio) for text, prio in zip(col, PRIORITIES[j])]
               for j, col in enumerate(L["actions"])]
    fig3, _ = executive_roadmap_quarters(
        QUARTERS,
        actions,
        title=L["roadmap_title"],
        caption=L["roadmap_caption"],
        source=L["roadmap_source"],
        priority_labels=L["priority_labels"],
    )
    fig3.savefig(OUT_DIR / f"plot3_roadmap_quarters.{loc}.png", dpi=160, bbox_inches="tight")


if __name__ == "__main__":
    for loc, L in LOCALES.items():
        render_locale(loc, L)
    set_source_prefix("Quelle: ")
    print(f"Rendered EN/PL eudr-update plots to {OUT_DIR}")
    for p in sorted(OUT_DIR.glob("*.??.png")):
        print(f"  {p.name} ({p.stat().st_size / 1024:.1f} KB)")
