"""Quality KPI Dashboard - Streamlit."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import yaml
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.kpis import calcular_kpis_globales, calcular_kpis_por_dimension, calcular_pareto, identificar_lote_critico
from src.capability import resumen_capacidad, calcular_cp_cpk

st.set_page_config(page_title="Quality KPI Dashboard", page_icon="📊", layout="wide")

@st.cache_data
def cargar_datos():
    df = pd.read_csv("data/calidad_muestra.csv")
    with open("config/quality_config.yaml") as f:
        config = yaml.safe_load(f)
    return df, config

df, config = cargar_datos()
kpis = calcular_kpis_globales(df)
capacidad = resumen_capacidad(df, config["variables_criticas"])

st.title("📊 Quality KPI Dashboard")
st.caption("2 líneas · 4 máquinas · 3 turnos · 250 lotes simulados · Metodología documentada en README")

# --- 3 KPIs críticos ---
c1, c2, c3 = st.columns(3)
c1.metric("FPY (First Pass Yield)", f"{kpis['fpy']:.1%}")
c2.metric("Tasa de Scrap", f"{kpis['tasa_scrap']:.2%}")
cpk_min = capacidad["cpk"].min()
c3.metric("Cpk crítico", f"{cpk_min:.2f}", capacidad.loc[capacidad["cpk"].idxmin(), "variable"])

st.divider()

# --- Gráfico 1: Tendencia ---
st.subheader("📈 Evolución de la tasa de defectos")
df_t = df.copy()
df_t["tasa_defectos"] = df_t["unidades_defectuosas"] / df_t["unidades_producidas"] * 100
fig1 = px.line(df_t, x="fecha", y="tasa_defectos", template="plotly_white")
st.plotly_chart(fig1, use_container_width=True)

col_a, col_b = st.columns(2)

# --- Gráfico 2: Pareto ---
with col_a:
    st.subheader("🔍 Pareto de defectos")
    pareto = calcular_pareto(df)
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(go.Bar(x=pareto["defecto"], y=pareto["frecuencia"], marker_color="steelblue"), secondary_y=False)
    fig2.add_trace(go.Scatter(x=pareto["defecto"], y=pareto["porcentaje_acumulado"], line=dict(color="red")), secondary_y=True)
    fig2.update_layout(template="plotly_white", showlegend=False, height=380)
    st.plotly_chart(fig2, use_container_width=True)

# --- Gráfico 3: Comparación por dimensión ---
with col_b:
    st.subheader("🏭 Comparación por dimensión")
    dim = st.selectbox("Agrupar por:", ["maquina", "turno", "linea", "operador"])
    comp = calcular_kpis_por_dimension(df, dim)
    fig3 = px.bar(comp, x=dim, y="tasa_defectos", color="tasa_defectos",
                   color_continuous_scale="Reds", template="plotly_white")
    fig3.update_layout(height=380, yaxis_tickformat=".1%")
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# --- Gráfico 4: Capacidad de proceso (Cp/Cpk) ---
st.subheader("📐 Capacidad de proceso (Cp/Cpk)")
col_c, col_d = st.columns(2)
for i, row in capacidad.iterrows():
    col = col_c if i == 0 else col_d
    with col:
        fig4 = px.histogram(df, x=row["columna"], nbins=30, template="plotly_white")
        fig4.add_vline(x=row["lsl"], line_dash="dash", line_color="red", annotation_text="LSL")
        fig4.add_vline(x=row["usl"], line_dash="dash", line_color="red", annotation_text="USL")
        fig4.update_layout(title=f"{row['variable']} — Cpk={row['cpk']} ({row['clasificacion']})", height=320)
        st.plotly_chart(fig4, use_container_width=True)

st.divider()

# --- Conclusiones accionables ---
st.subheader("✅ Conclusiones")
peor_maquina = calcular_kpis_por_dimension(df, "maquina").iloc[0]
peor_turno = calcular_kpis_por_dimension(df, "turno").iloc[0]
st.markdown(f"""
- **{peor_maquina['maquina']}** presenta la mayor tasa de defectos ({peor_maquina['tasa_defectos']:.1%}) — candidata prioritaria a mantenimiento preventivo.
- El turno **{peor_turno['turno']}** concentra la peor calidad ({peor_turno['tasa_defectos']:.1%}) — revisar supervisión/carga de trabajo.
- Cpk mínimo = **{cpk_min:.2f}** ({capacidad.loc[capacidad['cpk'].idxmin(),'variable']}) — proceso {'capaz' if cpk_min>=1.33 else 'marginal, requiere monitoreo' if cpk_min>=1 else 'NO capaz, acción correctiva urgente'}.
""")

st.caption("Datos 100% simulados con supuestos documentados en src/data_generator.py · Metodología Six Sigma para Cp/Cpk")
