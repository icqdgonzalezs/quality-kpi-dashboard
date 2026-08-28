"""
Industrial KPI Intelligence
============================

Industrial Operations Intelligence Platform.

La aplicación integra:

- Data Quality
- Control Center
- Plant Overview
- Executive KPIs
- Quality Performance
- Operational Analysis
- Process Capability
- Actionable Insights

Arquitectura:

    Dataset
       ↓
    Data Quality Gate
       ↓
    Control Center
       ↓
    Plant Overview
       ↓
    Analytical Engines
       ↓
    Decision Support
"""

from __future__ import annotations

import os
import sys

import pandas as pd
import streamlit as st
import yaml


# =====================================================================
# PROJECT PATH
# =====================================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(
        0,
        PROJECT_ROOT,
    )


# =====================================================================
# COMPONENTS
# =====================================================================

from dashboard.components.capability_charts import (
    renderizar_capability_dashboard,
)

from dashboard.components.charts import (
    renderizar_operational_analysis,
    renderizar_quality_performance,
)

from dashboard.components.filters import (
    aplicar_filtros,
)

from dashboard.components.insights import (
    renderizar_insights,
)

from dashboard.components.kpi_cards import (
    renderizar_kpis,
)

from dashboard.components.plant_overview import (
    renderizar_plant_overview,
)


# =====================================================================
# ANALYTICS ENGINE
# =====================================================================

from src.capability import (
    resumen_capacidad,
)

from src.kpis import (
    calcular_kpis_globales,
    identificar_lote_critico,
)

from src.validation import (
    obtener_reporte_validacion,
)


# =====================================================================
# STREAMLIT CONFIGURATION
# =====================================================================

st.set_page_config(
    page_title="Industrial KPI Intelligence",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================================================
# INDUSTRIAL HMI VISUAL SYSTEM
# =====================================================================

st.markdown(
    """
    <style>

    /* ================================================================
       GLOBAL
       ================================================================ */

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                rgba(56, 189, 248, 0.045),
                transparent 30%
            ),
            #0B1220;

        color: #E5E7EB;
    }

    .block-container {
        max-width: 1550px;
        padding-top: 1.35rem;
        padding-bottom: 3rem;
    }


    /* ================================================================
       HEADER
       ================================================================ */

    .platform-label {
        font-size: 0.70rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #64748B;
        margin-bottom: 0.25rem;
    }

    .hero-title {
        font-size: 2.60rem;
        font-weight: 780;
        line-height: 1.03;
        color: #F8FAFC;
        margin-bottom: 0.25rem;
    }

    .hero-subtitle {
        font-size: 0.96rem;
        color: #94A3B8;
        margin-bottom: 0.8rem;
    }


    /* ================================================================
       SECTION LABELS
       ================================================================ */

    .section-label {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        color: #64748B;
        margin-bottom: 0.2rem;
    }


    /* ================================================================
       METRICS
       ================================================================ */

    [data-testid="stMetric"] {
        background: #111827 !important;
        border: 1px solid #263247 !important;
        border-radius: 12px !important;
        padding: 0.90rem 1rem !important;

        box-shadow:
            0 2px 10px rgba(0, 0, 0, 0.24) !important;
    }

    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-weight: 650 !important;
    }

    [data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-weight: 760 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #CBD5E1 !important;
    }


    /* ================================================================
       SIDEBAR
       ================================================================ */

    [data-testid="stSidebar"] {
        background: #0B1220 !important;
        border-right: 1px solid #263247 !important;
    }

    [data-testid="stSidebar"] * {
        color: #E5E7EB;
    }

    [data-testid="stSidebar"] label {
        color: #CBD5E1 !important;
    }

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #64748B !important;
    }


    /* ================================================================
       BUTTONS
       ================================================================ */

    .stButton > button {
        border-radius: 8px;
        border: 1px solid #334155;
        background: #111827;
        color: #E5E7EB;
        font-weight: 650;
        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        border-color: #38BDF8;
        color: #F8FAFC;
        background: #162033;
    }


    /* ================================================================
       SELECT BOX
       ================================================================ */

    div[data-baseweb="select"] > div {
        background: #111827 !important;
        border-color: #334155 !important;
        border-radius: 8px !important;
        color: #E5E7EB !important;
    }


    /* ================================================================
       DATE INPUT
       ================================================================ */

    [data-testid="stDateInput"] input {
        background: #111827 !important;
        color: #E5E7EB !important;
    }


    /* ================================================================
       TABS
       ================================================================ */

    button[data-baseweb="tab"] {
        color: #94A3B8 !important;
        font-weight: 650;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #38BDF8 !important;
    }


    /* ================================================================
       DATAFRAME
       ================================================================ */

    [data-testid="stDataFrame"] {
        border: 1px solid #263247;
        border-radius: 10px;
        overflow: hidden;
    }


    /* ================================================================
       ALERTS
       ================================================================ */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* ================================================================
       DIVIDERS
       ================================================================ */

    hr {
        border-color: #263247 !important;
        margin-top: 1.2rem;
        margin-bottom: 1.2rem;
    }


    /* ================================================================
       CAPTIONS
       ================================================================ */

    [data-testid="stCaptionContainer"] {
        color: #64748B !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================================
# DATA LOADING
# =====================================================================

@st.cache_data
def cargar_datos() -> tuple[pd.DataFrame, dict]:
    """Carga el dataset y la configuración analítica."""

    ruta_datos = os.path.join(
        PROJECT_ROOT,
        "data",
        "calidad_muestra.csv",
    )

    ruta_config = os.path.join(
        PROJECT_ROOT,
        "config",
        "quality_config.yaml",
    )

    df = pd.read_csv(
        ruta_datos
    )

    df["fecha"] = pd.to_datetime(
        df["fecha"],
        errors="coerce",
    )

    with open(
        ruta_config,
        encoding="utf-8",
    ) as archivo:

        config = yaml.safe_load(
            archivo
        )

    return df, config


# =====================================================================
# LOAD
# =====================================================================

df, config = cargar_datos()


# =====================================================================
# DATA QUALITY GATE
# =====================================================================

reporte_validacion = obtener_reporte_validacion(
    df
)


if not reporte_validacion["valido"]:

    st.markdown(
        '<div class="section-label">'
        "SYSTEM VALIDATION"
        "</div>",
        unsafe_allow_html=True,
    )

    st.error(
        "DATA QUALITY GATE FAILED"
    )

    st.warning(
        "El dataset no cumple las reglas de calidad "
        "necesarias para ejecutar el análisis."
    )

    with st.expander(
        "Ver observaciones de calidad"
    ):

        for error in reporte_validacion[
            "errores"
        ]:

            st.error(error)

    st.stop()


# =====================================================================
# APPLICATION HEADER
# =====================================================================

st.markdown(
    '<div class="platform-label">'
    "INDUSTRIAL ANALYTICS PLATFORM"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-title">'
    "🏭 Industrial KPI Intelligence"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-subtitle">'
    "Industrial Operations Intelligence Platform · "
    "Quality · Reliability · Process Capability"
    "</div>",
    unsafe_allow_html=True,
)


# =====================================================================
# SYSTEM STATUS
# =====================================================================

status_1, status_2, status_3, status_4 = st.columns(4)


with status_1:

    st.metric(
        "SYSTEM",
        "ONLINE",
    )


with status_2:

    st.metric(
        "DATA QUALITY",
        "VALID",
    )


with status_3:

    st.metric(
        "EQUIPMENT",
        f"{df['equipo'].nunique()}",
    )


with status_4:

    st.metric(
        "LOTES",
        f"{df['lote'].nunique():,}",
    )


st.divider()


# =====================================================================
# CONTROL CENTER
# =====================================================================

df_filtrado = aplicar_filtros(
    df
)


# =====================================================================
# EMPTY DATA STATE
# =====================================================================

if df_filtrado.empty:

    st.markdown(
        '<div class="section-label">'
        "ANALYTICAL STATE"
        "</div>",
        unsafe_allow_html=True,
    )

    st.warning(
        "NO DATA FOR CURRENT SELECTION"
    )

    st.info(
        "La combinación de filtros no contiene observaciones. "
        "Amplía el período o modifica Línea, Equipo, Turno u Operador."
    )

    st.stop()


# =====================================================================
# ANALYTICAL CONTEXT
# =====================================================================

version_filtros = int(
    st.session_state.get(
        "filtros_reset_version",
        0,
    )
)

periodo_actual = st.session_state.get(
    "periodo_filtro_final",
    (
        df["fecha"].min().date(),
        df["fecha"].max().date(),
    ),
)

if isinstance(periodo_actual, (tuple, list)) and len(periodo_actual) == 2:
    fecha_inicio_contexto = periodo_actual[0]
    fecha_fin_contexto = periodo_actual[1]
else:
    fecha_inicio_contexto = df["fecha"].min().date()
    fecha_fin_contexto = df["fecha"].max().date()

linea_contexto = str(
    st.session_state.get(
        f"linea_filtro_final_{version_filtros}",
        "Todas",
    )
)

equipo_contexto = str(
    st.session_state.get(
        f"equipo_filtro_final_{version_filtros}",
        "Todos",
    )
)

turno_contexto = str(
    st.session_state.get(
        f"turno_filtro_final_{version_filtros}",
        "Todos",
    )
)

operador_contexto = str(
    st.session_state.get(
        f"operador_filtro_final_{version_filtros}",
        "Todos",
    )
)

st.markdown(
    '<div class="section-label">'
    "CONTEXTO ANALÍTICO"
    "</div>",
    unsafe_allow_html=True,
)

with st.container(border=True):

    st.markdown(
        "#### 🧭 Universo analítico activo"
    )

    st.caption(
        "Contexto correspondiente a la selección actual del Centro de control."
    )

    contexto_1, contexto_2, contexto_3 = st.columns(3)

    with contexto_1:
        st.metric(
            "Registros",
            f"{len(df_filtrado):,}",
        )

    with contexto_2:
        st.metric(
            "Lotes",
            f"{df_filtrado['lote'].nunique():,}",
        )

    with contexto_3:
        st.metric(
            "Equipos activos",
            f"{df_filtrado['equipo'].nunique():,}",
        )

    st.markdown("")

    detalle_1, detalle_2, detalle_3, detalle_4 = st.columns(4)

    with detalle_1:
        st.caption("📅 Período")
        st.write(
            f"{fecha_inicio_contexto.strftime('%d/%m/%Y')} "
            f"→ "
            f"{fecha_fin_contexto.strftime('%d/%m/%Y')}"
        )

    with detalle_2:
        st.caption("🏭 Línea")
        st.write(linea_contexto)

    with detalle_3:
        st.caption("⚙️ Equipo")
        st.write(equipo_contexto)

    with detalle_4:
        st.caption("🌙 Turno")
        st.write(turno_contexto)

    st.caption("👷 Operador")
    st.write(operador_contexto)


# =====================================================================
# PLANT OVERVIEW
# =====================================================================

renderizar_plant_overview(
    df_filtrado
)


st.divider()


# =====================================================================
# KPI ENGINE
# =====================================================================

kpis = calcular_kpis_globales(
    df_filtrado
)


# =====================================================================
# CAPABILITY ENGINE
# =====================================================================

capacidad = resumen_capacidad(
    df_filtrado,
    config["variables_criticas"],
)


cpk_validos = capacidad[
    capacidad["cpk"].notna()
].copy()


if cpk_validos.empty:

    cpk_min = None
    variable_cpk = "N/D"

else:

    indice_cpk = cpk_validos[
        "cpk"
    ].idxmin()

    cpk_min = float(
        cpk_validos.loc[
            indice_cpk,
            "cpk",
        ]
    )

    variable_cpk = str(
        cpk_validos.loc[
            indice_cpk,
            "variable",
        ]
    )


# =====================================================================
# CRITICAL LOT
# =====================================================================

lote_critico = identificar_lote_critico(
    df_filtrado
)


# =====================================================================
# EXECUTIVE KPI SUMMARY
# =====================================================================

renderizar_kpis(
    kpis=kpis,
    cpk_min=cpk_min,
    variable_cpk=variable_cpk,
    lote_critico=lote_critico,
)


st.divider()


# =====================================================================
# MONITORING NAVIGATION
# =====================================================================

st.sidebar.divider()

st.sidebar.markdown(
    "### 📡 Monitoring"
)

st.sidebar.caption(
    "Selecciona la perspectiva de análisis."
)


vista = st.sidebar.radio(
    "Vista",
    [
        "Executive Overview",
        "Quality Performance",
        "Operational Analysis",
        "Process Capability",
        "Data Quality",
    ],
    label_visibility="collapsed",
)


# =====================================================================
# EXECUTIVE OVERVIEW
# =====================================================================

if vista == "Executive Overview":

    renderizar_quality_performance(
        df_filtrado
    )

    st.divider()

    renderizar_operational_analysis(
        df_filtrado
    )

    st.divider()

    renderizar_insights(
        df_filtrado,
        cpk_min,
        variable_cpk,
    )


# =====================================================================
# QUALITY PERFORMANCE
# =====================================================================

elif vista == "Quality Performance":

    renderizar_quality_performance(
        df_filtrado
    )


# =====================================================================
# OPERATIONAL ANALYSIS
# =====================================================================

elif vista == "Operational Analysis":

    renderizar_operational_analysis(
        df_filtrado
    )

    st.divider()

    renderizar_insights(
        df_filtrado,
        cpk_min,
        variable_cpk,
    )


# =====================================================================
# PROCESS CAPABILITY
# =====================================================================

elif vista == "Process Capability":

    renderizar_capability_dashboard(
        df=df_filtrado,
        capacidad=capacidad,
        variables_config=config["variables_criticas"],
    )


# =====================================================================
# DATA QUALITY
# =====================================================================

elif vista == "Data Quality":

    st.markdown(
        '<div class="section-label">'
        "DATA QUALITY"
        "</div>",
        unsafe_allow_html=True,
    )

    st.subheader(
        "Data Quality Health Check"
    )

    st.caption(
        "Validaciones ejecutadas antes del procesamiento analítico."
    )


    dq1, dq2, dq3, dq4 = st.columns(4)


    with dq1:

        st.metric(
            "Estado",
            reporte_validacion[
                "estado"
            ],
        )


    with dq2:

        st.metric(
            "Completitud",
            f"{reporte_validacion['completitud']:.1%}",
        )


    with dq3:

        st.metric(
            "Celdas nulas",
            f"{reporte_validacion['celdas_nulas']:,}",
        )


    with dq4:

        st.metric(
            "Observaciones",
            reporte_validacion[
                "numero_errores"
            ],
        )


    st.success(
        "DATA QUALITY GATE PASSED"
    )

    st.caption(
        "La validación estructural y de negocio "
        "se ejecuta antes del análisis."
    )


# =====================================================================
# FOOTER
# =====================================================================

st.divider()

st.caption(
    "Industrial KPI Intelligence · "
    "Industrial Operations Intelligence Platform · "
    "Python · Pandas · NumPy · Plotly · Streamlit · "
    "Lean / Six Sigma"
)
