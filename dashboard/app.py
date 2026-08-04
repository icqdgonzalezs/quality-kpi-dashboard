import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Quality KPI Dashboard",
    page_icon="📊",
    layout="wide"
)

# Título y descripción
st.title("📊 Quality KPI Dashboard")
st.markdown("**Monitoreo de calidad en línea de producción – KPIs en tiempo real, Pareto y tendencias.**")

# Generar datos simulados
np.random.seed(42)
fechas = pd.date_range(start="2025-01-01", periods=100, freq='D')
data = pd.DataFrame({
    'fecha': fechas,
    'lote': [f'L{i}' for i in range(1, 101)],
    'unidades_producidas': np.random.randint(800, 1200, 100),
    'unidades_defectuosas': np.random.binomial(50, 0.08, 100),
    'defecto_tipo': np.random.choice(['Rayadura', 'Peso fuera', 'Largo fuera', 'Mancha'], 100)
})
data['tasa_defectos'] = data['unidades_defectuosas'] / data['unidades_producidas'] * 100

# KPIs principales
col1, col2, col3 = st.columns(3)
col1.metric("Tasa de defectos promedio", f"{data['tasa_defectos'].mean():.2f}%")
col2.metric("Lote con mayor defectos", data.loc[data['unidades_defectuosas'].idxmax(), 'lote'])
col3.metric("Total defectuosos", data['unidades_defectuosas'].sum())

# Gráfico de tendencia
st.subheader("📈 Evolución de la tasa de defectos")
fig1 = px.line(data, x='fecha', y='tasa_defectos', 
               labels={'tasa_defectos':'Tasa de defectos (%)'},
               template='plotly_white')
st.plotly_chart(fig1, use_container_width=True)

# Diagrama de Pareto
st.subheader("🔍 Diagrama de Pareto – Tipos de defecto")
pareto = data['defecto_tipo'].value_counts().reset_index()
pareto.columns = ['Defecto', 'Frecuencia']
pareto['Porcentaje'] = pareto['Frecuencia'] / pareto['Frecuencia'].sum() * 100
fig2 = px.bar(pareto, x='Defecto', y='Frecuencia', text='Porcentaje',
              labels={'Frecuencia':'Cantidad de defectos'},
              template='plotly_white',
              title='Distribución de defectos')
st.plotly_chart(fig2, use_container_width=True)

# Nota al pie
st.caption("Dashboard desarrollado con Python + Streamlit · Datos simulados para demostración")
