import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

# Diagrama de Pareto mejorado con línea acumulada y etiquetas de frecuencia
st.subheader("🔍 Diagrama de Pareto – Tipos de defecto")

# Preparar datos del Pareto
pareto_df = data['defecto_tipo'].value_counts().reset_index()
pareto_df.columns = ['Defecto', 'Frecuencia']
pareto_df = pareto_df.sort_values('Frecuencia', ascending=False)
pareto_df['Porcentaje'] = pareto_df['Frecuencia'] / pareto_df['Frecuencia'].sum() * 100
pareto_df['Porc_acumulado'] = pareto_df['Porcentaje'].cumsum()

# Crear figura con doble eje Y
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

# Barras con etiquetas de frecuencia
fig2.add_trace(
    go.Bar(x=pareto_df['Defecto'], y=pareto_df['Frecuencia'],
           name='Frecuencia', marker_color='steelblue',
           text=pareto_df['Frecuencia'],        # muestra el número sobre la barra
           textposition='outside'),
    secondary_y=False
)

# Línea acumulada
fig2.add_trace(
    go.Scatter(x=pareto_df['Defecto'], y=pareto_df['Porc_acumulado'],
               mode='lines+markers', name='% Acumulado',
               line=dict(color='red', width=2),
               marker=dict(size=8)),
    secondary_y=True
)

# Estilizar ejes
fig2.update_yaxes(title_text="Frecuencia", secondary_y=False)
fig2.update_yaxes(title_text="% Acumulado", secondary_y=True, range=[0, 105])
fig2.update_layout(
    title="Diagrama de Pareto - Tipos de defecto",
    template='plotly_white',
    hovermode='x unified'
)

st.plotly_chart(fig2, use_container_width=True)

# Nota al pie
st.caption("Dashboard desarrollado con Python + Streamlit · Datos simulados para demostración")