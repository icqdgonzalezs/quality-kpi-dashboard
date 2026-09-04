from __future__ import annotations

from dash import Input, Output


def actualizar_datos_filtrados(
    df,
    aplicar_filtros,
    start_date,
    end_date,
    linea,
    equipo,
    turno,
    operador,
):
    filtrado = aplicar_filtros(
        df,
        fecha_inicio=start_date,
        fecha_fin=end_date,
        linea=linea or "Todas",
        equipo=equipo or "Todos",
        turno=turno or "Todos",
        operador=operador or "Todos",
    )

    return filtrado.to_json(
        orient="split",
        date_format="iso",
    )


def registrar_callbacks_datos(
    app,
    df,
    aplicar_filtros,
) -> None:
    @app.callback(
        Output("store-datos-filtrados", "data"),
        Input("filtro-periodo", "start_date"),
        Input("filtro-periodo", "end_date"),
        Input("filtro-linea", "value"),
        Input("filtro-equipo", "value"),
        Input("filtro-turno", "value"),
        Input("filtro-operador", "value"),
    )
    def callback_actualizar_datos_filtrados(
        start_date,
        end_date,
        linea,
        equipo,
        turno,
        operador,
    ):
        return actualizar_datos_filtrados(
            df,
            aplicar_filtros,
            start_date,
            end_date,
            linea,
            equipo,
            turno,
            operador,
        )
