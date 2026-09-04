from __future__ import annotations

from dash import html


def crear_kpi_card(
    titulo: str,
    componente_id: str,
    valor_inicial: str = "—",
) -> html.Div:
    """Crea una KPI Card reutilizable para el dashboard Dash."""
    return html.Div(
        [
            html.Div(
                titulo,
                className="kpi-label",
            ),
            html.Div(
                valor_inicial,
                id=componente_id,
                className="kpi-value",
            ),
        ],
        className="kpi-card",
    )


def crear_kpi_grid() -> html.Div:
    """Construye la fila estándar de KPIs ejecutivos."""
    return html.Div(
        [
            crear_kpi_card(
                "PRODUCCIÓN TOTAL",
                "kpi-produccion-total",
                "—",
            ),
            crear_kpi_card(
                "FPY",
                "kpi-fpy",
                "—",
            ),
            crear_kpi_card(
                "TASA DE DEFECTOS",
                "kpi-defectos",
                "—",
            ),
            crear_kpi_card(
                "TASA DE SCRAP",
                "kpi-scrap",
                "—",
            ),
        ],
        className="kpi-grid",
    )
