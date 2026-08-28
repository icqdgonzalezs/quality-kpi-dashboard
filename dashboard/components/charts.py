"""Visualizaciones analíticas del dashboard."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from src.kpis import (
    calcular_kpis_por_dimension,
    calcular_pareto,
)

from dashboard.components.theme import (
    CHART_COLORS,
    COLORS,
    PLOTLY_LAYOUT,
)


# =====================================================================
# CONTEXTO ANALÍTICO
# =====================================================================

def _obtener_contexto_dimension() -> dict:
    """
    Obtiene los filtros activos del Control Center para contextualizar
    las visualizaciones.

    No modifica el estado de Streamlit.
    """

    version = int(
        st.session_state.get(
            "filtros_reset_version",
            0,
        )
    )

    return {
        "linea": str(
            st.session_state.get(
                f"linea_filtro_final_{version}",
                "Todas",
            )
        ),
        "equipo": str(
            st.session_state.get(
                f"equipo_filtro_final_{version}",
                "Todos",
            )
        ),
        "turno": str(
            st.session_state.get(
                f"turno_filtro_final_{version}",
                "Todos",
            )
        ),
        "operador": str(
            st.session_state.get(
                f"operador_filtro_final_{version}",
                "Todos",
            )
        ),
    }


def _resumir_contexto(
    contexto: dict,
) -> str:
    """Construye una descripción compacta del universo analítico."""

    elementos = []

    if contexto["linea"] != "Todas":
        elementos.append(
            f"Línea: {contexto['linea']}"
        )

    if contexto["equipo"] != "Todos":
        elementos.append(
            f"Equipo: {contexto['equipo']}"
        )

    if contexto["turno"] != "Todos":
        elementos.append(
            f"Turno: {contexto['turno']}"
        )

    if contexto["operador"] != "Todos":
        elementos.append(
            f"Operador: {contexto['operador']}"
        )

    if not elementos:
        return "Todas las operaciones"

    return " · ".join(elementos)


def _nombre_dimension(
    dimension: str,
) -> str:
    """Convierte el nombre técnico de una dimensión a nombre visible."""

    return {
        "equipo": "Equipo",
        "turno": "Turno",
        "operador": "Operador",
        "linea": "Línea",
        "maquina": "Máquina",
    }[dimension]


# =====================================================================
# QUALITY PERFORMANCE
# =====================================================================

def renderizar_quality_performance(
    df: pd.DataFrame,
) -> None:
    """Renderiza la tendencia temporal de calidad."""

    st.markdown(
        '<div class="section-label">QUALITY PERFORMANCE</div>',
        unsafe_allow_html=True,
    )

    st.subheader(
        "Evolución de la calidad"
    )

    st.caption(
        "Seguimiento temporal de la tasa de defectos."
    )

    datos = df.copy()

    datos["tasa_defectos"] = (
        datos["unidades_defectuosas"]
        / datos["unidades_producidas"]
        * 100
    )

    tendencia = (
        datos
        .groupby(
            "fecha",
            as_index=False,
        )["tasa_defectos"]
        .mean()
        .sort_values("fecha")
    )

    fig = px.line(
        tendencia,
        x="fecha",
        y="tasa_defectos",
        markers=True,
    )

    fig.update_traces(
        line={
            "color": CHART_COLORS["trend"],
            "width": 3,
        },
        marker={
            "size": 6,
        },
    )

    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=450,
        xaxis_title="Fecha",
        yaxis_title="Tasa de defectos (%)",
        hovermode="x unified",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )


# =====================================================================
# OPERATIONAL ANALYSIS
# =====================================================================

def renderizar_operational_analysis(
    df: pd.DataFrame,
) -> None:
    """Renderiza Pareto y comparación operacional."""

    st.markdown(
        '<div class="section-label">OPERATIONAL ANALYSIS</div>',
        unsafe_allow_html=True,
    )

    st.subheader(
        "Diagnóstico operacional"
    )

    izquierda, derecha = st.columns(2)

    # ---------------------------------------------------------------
    # PARETO
    # ---------------------------------------------------------------

    with izquierda:

        st.markdown(
            "#### 🔍 Pareto de defectos"
        )

        pareto = calcular_pareto(df)

        if pareto.empty:

            st.success(
                "No existen unidades defectuosas "
                "en la selección."
            )

        else:

            figura = make_subplots(
                specs=[
                    [{"secondary_y": True}]
                ]
            )

            figura.add_trace(
                go.Bar(
                    x=pareto["defecto"],
                    y=pareto["frecuencia"],
                    name="Defectuosas",
                    marker_color=CHART_COLORS[
                        "pareto_bar"
                    ],
                ),
                secondary_y=False,
            )

            figura.add_trace(
                go.Scatter(
                    x=pareto["defecto"],
                    y=pareto[
                        "porcentaje_acumulado"
                    ],
                    mode="lines+markers",
                    name="% acumulado",
                    line={
                        "color": CHART_COLORS[
                            "pareto_line"
                        ],
                        "width": 3,
                    },
                ),
                secondary_y=True,
            )

            figura.add_hline(
                y=80,
                line_dash="dot",
                line_color=COLORS["reference"],
                annotation_text="80%",
                secondary_y=True,
            )

            figura.update_layout(
                **PLOTLY_LAYOUT,
                height=440,
                hovermode="x unified",
            )

            figura.update_yaxes(
                title_text="Unidades",
                secondary_y=False,
            )

            figura.update_yaxes(
                title_text="% acumulado",
                range=[0, 105],
                secondary_y=True,
            )

            st.plotly_chart(
                figura,
                width="stretch",
            )

    # ---------------------------------------------------------------
    # DIMENSIÓN
    # ---------------------------------------------------------------

    with derecha:

        st.markdown(
            "#### 📊 Perspectiva de análisis"
        )

        st.caption(
            "Selecciona la dimensión con la que quieres comparar "
            "el universo actualmente filtrado."
        )

        contexto = _obtener_contexto_dimension()

        contexto_visible = _resumir_contexto(
            contexto
        )

        st.caption(
            "UNIVERSO ANALIZADO"
        )

        st.markdown(
            f"**{contexto_visible}**"
        )

        dimension = st.selectbox(
            "Dimensión",
            [
                "equipo",
                "turno",
                "operador",
                "linea",
            ],
            format_func=_nombre_dimension,
            key="perspectiva_dimension",
        )

        nombre_dimension = _nombre_dimension(
            dimension
        )

        resultado = calcular_kpis_por_dimension(
            df,
            dimension,
        )

        if resultado.empty:

            st.info(
                "No hay observaciones para la dimensión seleccionada."
            )

        else:

            resultado = resultado.sort_values(
                "tasa_defectos",
                ascending=False,
            )

            colores = []

            promedio = resultado[
                "tasa_defectos"
            ].mean()

            desviacion = resultado[
                "tasa_defectos"
            ].std(ddof=0)

            for valor in resultado[
                "tasa_defectos"
            ]:

                if desviacion == 0:

                    estado = (
                        "NORMAL"
                        if valor <= promedio
                        else "WATCH"
                    )

                elif valor <= (
                    promedio + 0.5 * desviacion
                ):

                    estado = "NORMAL"

                elif valor <= (
                    promedio + desviacion
                ):

                    estado = "WATCH"

                else:

                    estado = "PRIORITY"

                colores.append(
                    {
                        "NORMAL": COLORS["normal"],
                        "WATCH": COLORS["warning"],
                        "PRIORITY": COLORS["critical"],
                    }[estado]
                )

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=resultado[dimension],
                    y=resultado["tasa_defectos"],
                    marker_color=colores,
                    text=[
                        f"{valor:.2%}"
                        for valor in resultado[
                            "tasa_defectos"
                        ]
                    ],
                    textposition="outside",
                    hovertemplate=(
                        f"{nombre_dimension}: "
                        "%{x}<br>"
                        "Tasa de defectos: %{y:.2%}"
                        "<extra></extra>"
                    ),
                )
            )

            fig.update_layout(
                **PLOTLY_LAYOUT,
                height=440,
                showlegend=False,
                title={
                    "text": (
                        f"Tasa de defectos por "
                        f"{nombre_dimension.lower()}"
                    ),
                    "x": 0.02,
                    "xanchor": "left",
                    "font": {
                        "size": 16,
                    },
                },
                xaxis_title=nombre_dimension,
                yaxis_title="Tasa de defectos",
            )

            fig.update_yaxes(
                tickformat=".1%",
            )

            st.plotly_chart(
                fig,
                width="stretch",
            )

            st.caption(
                f"Comparación por {nombre_dimension.lower()} · "
                f"{len(df):,} registros en el universo actual."
            )
