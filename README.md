# 📊 Quality KPI Dashboard

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.26.0-red?logo=streamlit)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**Panel interactivo de monitoreo de calidad para líneas de producción.**

---

## 🎯 Visión General

Herramienta diseñada para ingenieros de calidad y supervisores de producción que necesitan visualizar KPIs críticos en tiempo real. Simula el monitoreo de una línea de producción, calculando indicadores de defectos, capacidad de proceso (Cp/Cpk) y generando diagramas de Pareto para facilitar la toma de decisiones basada en datos.

---

## 📈 KPIs Implementados

| Indicador | Descripción |
|-----------|-------------|
| **Tasa de defectos (%)** | Porcentaje de unidades defectuosas por lote |
| **Total defectuosos** | Conteo absoluto de unidades con defectos |
| **Lote crítico** | Identificación del lote con mayor número de defectos |
| **Diagrama de Pareto** | Frecuencia de defectos por tipo (80/20) |
| **Evolución temporal** | Tendencia de la tasa de defectos a lo largo del tiempo |

---

## 🛠️ Stack Tecnológico

| Herramienta | Uso |
|-------------|-----|
| **Python 3.9+** | Lenguaje principal |
| **Streamlit** | Framework para dashboard interactivo |
| **Plotly Express** | Gráficos interactivos (líneas, barras) |
| **Pandas** | Manipulación y análisis de datos |
| **NumPy** | Cálculos numéricos y generación de datos simulados |

---

## 📸 Captura del Panel

![Panel de Control de Calidad](imagenes/panel_vista_previa.png)

---

## ⚙️ Instalación y Ejecución

```bash
# Clonar el repositorio
git clone https://github.com/icqdgonzalezs/quality-kpi-dashboard.git
cd quality-kpi-dashboard

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar panel
streamlit run dashboard/app.py
