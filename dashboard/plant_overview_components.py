from __future__ import annotations

from dash import html


def crear_tarjeta_equipo(
    equipo: str,
) -> html.Div:
    """Crea la estructura visual base de una tarjeta de equipo."""
    return html.Div(
        [
            html.Div(
                equipo,
                className="plant-equipment-id",
            ),
            html.Div(
                "—",
                className="plant-equipment-defect-rate",
            ),
            html.Div(
                "SIN DATOS",
                className="plant-equipment-status",
            ),
            html.Div(
                "0 lotes · 0 defectuosas",
                className="plant-equipment-detail",
            ),
        ],
        id={
            "type": "plant-equipment-card",
            "equipment": equipo,
        },
        className="plant-equipment-card",
    )


def crear_plant_overview(
    equipos: list[str] | None = None,
) -> html.Div:
    """Crea la sección visual de Plant Overview."""
    equipos = equipos or []

    return html.Div(
        [
            html.Div(
                "PLANT OVERVIEW",
                className="section-label",
            ),
            html.H3(
                "Estado operacional de equipos",
                className="section-title",
            ),
            html.P(
                "Estado relativo al desempeño observado "
                "en el universo seleccionado.",
                className="section-caption",
            ),
            html.Div(
                [
                    crear_tarjeta_equipo(equipo)
                    for equipo in equipos
                ],
                id="plant-equipment-grid",
                className="plant-equipment-grid",
            ),
        ],
        id="plant-overview",
        className="dashboard-section plant-overview",
    )
