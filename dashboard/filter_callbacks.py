from __future__ import annotations

from typing import Callable

import pandas as pd
from dash import Input, Output


_DF: pd.DataFrame | None = None
_APLICAR_FILTROS: Callable | None = None


def configurar_callbacks_filtros(
    df: pd.DataFrame,
    aplicar_filtros: Callable,
) -> None:
    global _DF, _APLICAR_FILTROS

    _DF = df
    _APLICAR_FILTROS = aplicar_filtros


def _obtener_dependencias() -> tuple[pd.DataFrame, Callable]:
    if _DF is None or _APLICAR_FILTROS is None:
        raise RuntimeError(
            "Los callbacks de filtros no han sido configurados."
        )

    return _DF, _APLICAR_FILTROS


def _filtrar_por_periodo(start_date, end_date):
    df, aplicar_filtros = _obtener_dependencias()

    return aplicar_filtros(
        df,
        fecha_inicio=start_date,
        fecha_fin=end_date,
    )


def actualizar_lineas(start_date, end_date):
    filtrado = _filtrar_por_periodo(start_date, end_date)

    opciones = [
        {"label": "Todas", "value": "Todas"},
        *[
            {"label": valor, "value": valor}
            for valor in sorted(
                filtrado["linea"].dropna().astype(str).unique()
            )
        ],
    ]

    return opciones, "Todas"


def actualizar_equipos(linea, start_date, end_date):
    df, aplicar_filtros = _obtener_dependencias()

    filtrado = aplicar_filtros(
        df,
        fecha_inicio=start_date,
        fecha_fin=end_date,
        linea=linea or "Todas",
    )

    opciones = [
        {"label": "Todos", "value": "Todos"},
        *[
            {"label": valor, "value": valor}
            for valor in sorted(
                filtrado["equipo"].dropna().astype(str).unique()
            )
        ],
    ]

    return opciones, "Todos"


def actualizar_turnos(equipo, linea, start_date, end_date):
    df, aplicar_filtros = _obtener_dependencias()

    filtrado = aplicar_filtros(
        df,
        fecha_inicio=start_date,
        fecha_fin=end_date,
        linea=linea or "Todas",
        equipo=equipo or "Todos",
    )

    opciones = [
        {"label": "Todos", "value": "Todos"},
        *[
            {"label": valor, "value": valor}
            for valor in sorted(
                filtrado["turno"].dropna().astype(str).unique()
            )
        ],
    ]

    return opciones, "Todos"


def actualizar_operadores(
    turno,
    equipo,
    linea,
    start_date,
    end_date,
):
    df, aplicar_filtros = _obtener_dependencias()

    filtrado = aplicar_filtros(
        df,
        fecha_inicio=start_date,
        fecha_fin=end_date,
        linea=linea or "Todas",
        equipo=equipo or "Todos",
        turno=turno or "Todos",
    )

    opciones = [
        {"label": "Todos", "value": "Todos"},
        *[
            {"label": valor, "value": valor}
            for valor in sorted(
                filtrado["operador"].dropna().astype(str).unique()
            )
        ],
    ]

    return opciones, "Todos"


def registrar_callbacks_filtros(
    app,
    df: pd.DataFrame,
    aplicar_filtros: Callable,
) -> None:
    configurar_callbacks_filtros(df, aplicar_filtros)

    @app.callback(
        Output("filtro-linea", "options"),
        Output("filtro-linea", "value"),
        Input("filtro-periodo", "start_date"),
        Input("filtro-periodo", "end_date"),
    )
    def callback_actualizar_lineas(start_date, end_date):
        return actualizar_lineas(start_date, end_date)

    @app.callback(
        Output("filtro-equipo", "options"),
        Output("filtro-equipo", "value"),
        Input("filtro-linea", "value"),
        Input("filtro-periodo", "start_date"),
        Input("filtro-periodo", "end_date"),
    )
    def callback_actualizar_equipos(linea, start_date, end_date):
        return actualizar_equipos(linea, start_date, end_date)

    @app.callback(
        Output("filtro-turno", "options"),
        Output("filtro-turno", "value"),
        Input("filtro-equipo", "value"),
        Input("filtro-linea", "value"),
        Input("filtro-periodo", "start_date"),
        Input("filtro-periodo", "end_date"),
    )
    def callback_actualizar_turnos(
        equipo,
        linea,
        start_date,
        end_date,
    ):
        return actualizar_turnos(
            equipo,
            linea,
            start_date,
            end_date,
        )

    @app.callback(
        Output("filtro-operador", "options"),
        Output("filtro-operador", "value"),
        Input("filtro-turno", "value"),
        Input("filtro-equipo", "value"),
        Input("filtro-linea", "value"),
        Input("filtro-periodo", "start_date"),
        Input("filtro-periodo", "end_date"),
    )
    def callback_actualizar_operadores(
        turno,
        equipo,
        linea,
        start_date,
        end_date,
    ):
        return actualizar_operadores(
            turno,
            equipo,
            linea,
            start_date,
            end_date,
        )
