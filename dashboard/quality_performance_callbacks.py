from __future__ import annotations

from io import StringIO

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output

from dashboard.kpi_presenter import formatear_kpis
from src.kpis import (
    calcular_kpis_globales,
    calcular_pareto,
    identificar_lote_critico,
)


def _leer_dataframe_filtrado(data):
    if not data:
        return pd.DataFrame()

    return pd.read_json(
        StringIO(data),
        orient="split",
    )


def actualizar_quality_performance(data):
    filtrado = _leer_dataframe_filtrado(data)

    if filtrado.empty:
        return "—", "—", "—", "—"

    kpis = calcular_kpis_globales(filtrado)
    presentados = formatear_kpis(kpis)

    return (
        presentados["fpy"],
        presentados["defectos"],
        presentados["scrap"],
        presentados["reproceso"],
    )


def crear_figura_pareto(filtrado):
    pareto = calcular_pareto(filtrado)

    if pareto.empty:
        return go.Figure()

    figura = go.Figure()

    figura.add_bar(
        x=pareto["defecto"],
        y=pareto["frecuencia"],
        name="Defectos",
    )

    figura.add_scatter(
        x=pareto["defecto"],
        y=pareto["porcentaje_acumulado"],
        name="% acumulado",
        mode="lines+markers",
        yaxis="y2",
    )

    figura.update_layout(
        title="Pareto de defectos",
        yaxis_title="Unidades defectuosas",
        yaxis2=dict(
            title="% acumulado",
            overlaying="y",
            side="right",
            range=[0, 100],
        ),
    )

    return figura


def crear_lote_critico(filtrado):
    if filtrado.empty:
        return "Sin datos para identificar un lote crítico."

    lote_critico = identificar_lote_critico(filtrado)

    return (
        f"Lote crítico: {lote_critico['lote']} "
        f"· Tasa de defectos: "
        f"{lote_critico['tasa_defectos_lote']:.1%}"
    )


def registrar_callbacks_quality_performance(app) -> None:
    @app.callback(
        Output("quality-fpy", "children"),
        Output("quality-defect-rate", "children"),
        Output("quality-scrap-rate", "children"),
        Output("quality-rework-rate", "children"),
        Output("quality-pareto", "children"),
        Output("quality-critical-lot", "children"),
        Input("store-datos-filtrados", "data"),
    )
    def callback_actualizar_quality_performance(data):
        metricas = actualizar_quality_performance(data)

        filtrado = _leer_dataframe_filtrado(data)

        if filtrado.empty:
            figura_pareto = go.Figure()
        else:
            figura_pareto = crear_figura_pareto(filtrado)

        if filtrado.empty:
            lote_critico = "Sin datos para identificar un lote crítico."
        else:
            lote_critico = crear_lote_critico(filtrado)

        return (
            *metricas,
            figura_pareto,
            lote_critico,
        )
