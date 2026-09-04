from __future__ import annotations

from dash import dcc, html


def crear_control_center(
    fechas: tuple,
    lineas: list[str],
    equipos: list[str],
    turnos: list[str],
    operadores: list[str],
) -> html.Div:
    return html.Div(
        [
            html.Div(
                [
                    html.H3("🎛️ Control Center"),
                    html.P(
                        "Define el universo operativo que quieres analizar."
                    ),
                ],
                className="section-header",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Período"),
                            dcc.DatePickerRange(
                                id="filtro-periodo",
                                start_date=fechas[0],
                                end_date=fechas[1],
                                min_date_allowed=fechas[0],
                                max_date_allowed=fechas[1],
                                display_format="YYYY-MM-DD",
                            ),
                        ],
                        className="filter-control",
                    ),
                    html.Div(
                        [
                            html.Label("Línea"),
                            dcc.Dropdown(
                                id="filtro-linea",
                                options=[
                                    {"label": value, "value": value}
                                    for value in lineas
                                ],
                                value="Todas",
                                clearable=False,
                            ),
                        ],
                        className="filter-control",
                    ),
                    html.Div(
                        [
                            html.Label("Equipo"),
                            dcc.Dropdown(
                                id="filtro-equipo",
                                options=[
                                    {"label": value, "value": value}
                                    for value in equipos
                                ],
                                value="Todos",
                                clearable=False,
                            ),
                        ],
                        className="filter-control",
                    ),
                    html.Div(
                        [
                            html.Label("Turno"),
                            dcc.Dropdown(
                                id="filtro-turno",
                                options=[
                                    {"label": value, "value": value}
                                    for value in turnos
                                ],
                                value="Todos",
                                clearable=False,
                            ),
                        ],
                        className="filter-control",
                    ),
                    html.Div(
                        [
                            html.Label("Operador"),
                            dcc.Dropdown(
                                id="filtro-operador",
                                options=[
                                    {"label": value, "value": value}
                                    for value in operadores
                                ],
                                value="Todos",
                                clearable=False,
                            ),
                        ],
                        className="filter-control",
                    ),
                    html.Button(
                        "↩️ Restaurar filtros",
                        id="btn-reset-filtros",
                        n_clicks=0,
                        className="control-button",
                    ),
                ],
                className="control-grid",
            ),
        ],
        className="control-center",
    )
