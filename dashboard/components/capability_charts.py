"""Visualización profesional de capacidad de proceso."""

from __future__ import annotations

import math

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from dashboard.components.theme import (
    CHART_COLORS,
    COLORS,
)


# =====================================================================
# UTILIDADES
# =====================================================================

def _estado_capacidad(
    clasificacion: str,
) -> str:
    """Normaliza la clasificación de capacidad."""

    texto = str(
        clasificacion
    ).lower()

    if "excelente" in texto:
        return "EXCELLENT"

    if (
        "capaz" in texto
        and "no capaz" not in texto
    ):
        return "CAPABLE"

    if "marginal" in texto:
        return "WATCH"

    if "no capaz" in texto:
        return "PRIORITY"

    if "insuficientes" in texto:
        return "NO DATA"

    if "inválidos" in texto:
        return "NO DATA"

    if "sin variabilidad" in texto:
        return "SPECIAL"

    return "INFO"


def _color_estado(
    estado: str,
) -> str:
    """Devuelve el color semántico del estado."""

    return {
        "EXCELLENT": COLORS["normal"],
        "CAPABLE": COLORS["normal"],
        "WATCH": COLORS["warning"],
        "PRIORITY": COLORS["critical"],
        "NO DATA": COLORS["reference"],
        "SPECIAL": COLORS["info"],
        "INFO": COLORS["info"],
    }.get(
        estado,
        COLORS["reference"],
    )


def _mensaje_estado(
    estado: str,
) -> str:
    """Devuelve una interpretación del estado."""

    return {
        "EXCELLENT": (
            "El proceso presenta una capacidad robusta "
            "respecto de las especificaciones."
        ),
        "CAPABLE": (
            "El proceso cumple el criterio de capacidad "
            "establecido para Cpk."
        ),
        "WATCH": (
            "El proceso requiere seguimiento para reducir "
            "el riesgo de incumplimiento."
        ),
        "PRIORITY": (
            "El proceso no demuestra capacidad suficiente. "
            "Se recomienda priorizar la investigación."
        ),
        "NO DATA": (
            "No existe información suficiente para evaluar "
            "la capacidad."
        ),
        "SPECIAL": (
            "El proceso presenta una condición especial "
            "que requiere interpretación adicional."
        ),
        "INFO": (
            "Revisar los indicadores estadísticos disponibles."
        ),
    }.get(
        estado,
        "Revisar los indicadores estadísticos.",
    )


def _formatear_indice(
    valor,
) -> str:
    """Formatea Cp/Cpk incluyendo valores infinitos."""

    if valor is None:
        return "N/D"

    try:
        valor_float = float(valor)

        if math.isinf(valor_float):
            return "∞"

        return f"{valor_float:.2f}"

    except (TypeError, ValueError):
        return "N/D"


# =====================================================================
# GRÁFICO
# =====================================================================

def _crear_grafico_capacidad(
    serie: pd.Series,
    lsl: float,
    usl: float,
    media: float | None,
    nominal: float | None,
    nombre_variable: str,
) -> go.Figure:
    """Construye distribución observada con especificaciones."""

    figura = go.Figure()

    figura.add_trace(
        go.Histogram(
            x=serie,
            nbinsx=24,
            name="Observaciones",
            marker_color=CHART_COLORS["trend"],
            opacity=0.82,
            hovertemplate=(
                f"{nombre_variable}<br>"
                "Valor: %{x}<br>"
                "Frecuencia: %{y}"
                "<extra></extra>"
            ),
        )
    )

    figura.add_vline(
        x=lsl,
        line_color=CHART_COLORS["specification"],
        line_width=3,
        line_dash="dash",
        annotation_text="LSL",
        annotation_position="top left",
    )

    figura.add_vline(
        x=usl,
        line_color=CHART_COLORS["specification"],
        line_width=3,
        line_dash="dash",
        annotation_text="USL",
        annotation_position="top right",
    )

    if nominal is not None and math.isfinite(nominal):
        figura.add_vline(
            x=nominal,
            line_color=CHART_COLORS["nominal"],
            line_width=2,
            line_dash="dot",
            annotation_text="Nominal",
            annotation_position="bottom",
        )

    if media is not None and math.isfinite(media):
        figura.add_vline(
            x=media,
            line_color=CHART_COLORS["mean"],
            line_width=2,
            annotation_text="Media",
            annotation_position="top",
        )

    figura.update_layout(
        height=430,
        margin={
            "l": 55,
            "r": 25,
            "t": 55,
            "b": 55,
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={
            "family": "Arial",
            "color": "#1F2937",
        },
        showlegend=False,
        xaxis_title=nombre_variable,
        yaxis_title="Frecuencia",
        bargap=0.05,
    )

    return figura


# =====================================================================
# COMPONENTE PRINCIPAL
# =====================================================================

def renderizar_capability_dashboard(
    df: pd.DataFrame,
    capacidad: pd.DataFrame,
    variables_config: dict,
) -> None:
    """Renderiza el análisis profesional de capacidad."""

    st.markdown(
        '<div class="section-label">'
        "PROCESS CAPABILITY"
        "</div>",
        unsafe_allow_html=True,
    )

    st.subheader(
        "Análisis Cp/Cpk"
    )

    st.caption(
        "Evaluación de capacidad respecto de los límites "
        "de especificación definidos en configuración."
    )

    if capacidad.empty:
        st.info(
            "No existen variables disponibles para evaluar."
        )
        return

    # ===============================================================
    # RESUMEN EJECUTIVO
    # ===============================================================

    cpk = pd.to_numeric(
        capacidad["cpk"],
        errors="coerce",
    ).dropna()

    cpk_min = (
        float(cpk.min())
        if not cpk.empty
        else None
    )

    marginales = int(
        capacidad["clasificacion"]
        .astype(str)
        .str.contains(
            "Marginal",
            case=False,
            na=False,
        )
        .sum()
    )

    no_capaces = int(
        capacidad["clasificacion"]
        .astype(str)
        .str.contains(
            "No capaz",
            case=False,
            na=False,
        )
        .sum()
    )

    r1, r2, r3, r4 = st.columns(4)

    with r1:
        st.metric(
            "Variables evaluadas",
            str(len(capacidad)),
        )

    with r2:
        st.metric(
            "Cpk mínimo",
            (
                f"{cpk_min:.2f}"
                if cpk_min is not None
                else "N/D"
            ),
        )

    with r3:
        st.metric(
            "Variables marginales",
            str(marginales),
        )

    with r4:
        st.metric(
            "Variables no capaces",
            str(no_capaces),
        )

    st.divider()

    # ===============================================================
    # PESTAÑAS POR VARIABLE
    # ===============================================================

    tabs = st.tabs(
        [
            str(row["variable"])
            for _, row in capacidad.iterrows()
        ]
    )

    for tab, (_, row) in zip(
        tabs,
        capacidad.iterrows(),
    ):

        with tab:

            variable = str(
                row["variable"]
            )

            columna = str(
                row["columna"]
            )

            serie = pd.to_numeric(
                df[columna],
                errors="coerce",
            ).dropna()

            lsl = float(
                row["lsl"]
            )

            usl = float(
                row["usl"]
            )

            media = (
                float(row["media"])
                if pd.notna(row["media"])
                else None
            )

            sigma = (
                float(row["sigma"])
                if pd.notna(row["sigma"])
                else None
            )

            estado = _estado_capacidad(
                str(row["clasificacion"])
            )

            mensaje = _mensaje_estado(
                estado
            )

            m1, m2, m3, m4 = st.columns(4)

            with m1:
                st.metric(
                    "Cp",
                    _formatear_indice(
                        row["cp"]
                    ),
                )

            with m2:
                st.metric(
                    "Cpk",
                    _formatear_indice(
                        row["cpk"]
                    ),
                )

            with m3:
                st.metric(
                    "Media",
                    (
                        f"{media:.3f}"
                        if media is not None
                        else "N/D"
                    ),
                )

            with m4:
                st.metric(
                    "σ",
                    (
                        f"{sigma:.4f}"
                        if sigma is not None
                        else "N/D"
                    ),
                )

            if estado in {
                "EXCELLENT",
                "CAPABLE",
            }:

                st.success(
                    f"{row['clasificacion']} · {mensaje}"
                )

            elif estado == "WATCH":

                st.warning(
                    f"{row['clasificacion']} · {mensaje}"
                )

            elif estado == "PRIORITY":

                st.error(
                    f"{row['clasificacion']} · {mensaje}"
                )

            else:

                st.info(
                    f"{row['clasificacion']} · {mensaje}"
                )

            st.markdown(
                "#### Especificaciones"
            )

            nominal = None

            configuracion_variable = (
                variables_config.get(
                    columna,
                    {},
                )
            )

            if (
                configuracion_variable.get(
                    "nominal"
                )
                is not None
            ):

                nominal = float(
                    configuracion_variable[
                        "nominal"
                    ]
                )

            if nominal is None:
                nominal = (lsl + usl) / 2

            s1, s2, s3 = st.columns(3)

            with s1:
                st.metric(
                    "LSL",
                    f"{lsl:.3f}",
                )

            with s2:
                st.metric(
                    "Nominal",
                    f"{nominal:.3f}",
                )

            with s3:
                st.metric(
                    "USL",
                    f"{usl:.3f}",
                )

            st.markdown(
                "#### Distribución del proceso"
            )

            if len(serie) < 2:

                st.info(
                    "No existen suficientes observaciones "
                    "para visualizar la distribución."
                )

            else:

                figura = _crear_grafico_capacidad(
                    serie=serie,
                    lsl=lsl,
                    usl=usl,
                    media=media,
                    nominal=nominal,
                    nombre_variable=variable,
                )

                st.plotly_chart(
                    figura,
                    width="stretch",
                )

            st.caption(
                f"{len(serie):,} observaciones utilizadas "
                "en el cálculo."
            )

    # ===============================================================
    # TABLA TÉCNICA
    # ===============================================================

    st.divider()

    st.markdown(
        "#### Resumen técnico"
    )

    columnas = [
        "variable",
        "lsl",
        "usl",
        "cp",
        "cpk",
        "media",
        "sigma",
        "n",
        "clasificacion",
    ]

    tabla = capacidad[
        [
            columna
            for columna in columnas
            if columna in capacidad.columns
        ]
    ].copy()

    st.dataframe(
        tabla,
        width="stretch",
        hide_index=True,
    )
