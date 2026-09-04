from __future__ import annotations

from dash import dcc, html

from dashboard.components_dash import crear_control_center
from dashboard.kpi_components import crear_kpi_grid
from dashboard.quality_performance_components import crear_quality_performance


def crear_app_layout(
    fecha_min: str,
    fecha_max: str,
    lineas: list[str],
    equipos: list[str],
    turnos: list[str],
    operadores: list[str],
):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        "INDUSTRIAL ANALYTICS PLATFORM",
                        className="platform-label",
                    ),
                    html.H1(
                        "🏭 Industrial KPI Intelligence",
                        className="hero-title",
                    ),
                    html.P(
                        "Industrial Operations Intelligence Platform · "
                        "Quality · Reliability · Process Capability",
                        className="hero-subtitle",
                    ),
                ],
                className="app-header",
            ),
            dcc.Store(
                id="store-datos-filtrados",
                storage_type="memory",
            ),
            crear_kpi_grid(),
            crear_quality_performance(),
            crear_control_center(
                (
                    fecha_min,
                    fecha_max,
                ),
                lineas,
                equipos,
                turnos,
                operadores,
            ),
        ]
    )
