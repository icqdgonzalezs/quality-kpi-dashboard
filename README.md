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

## 📸 Capturas del Panel

### Evolución de la tasa de defectos
![Evolución de la tasa de defectos](imagenes/panel_vista_previa1.png)

### Diagrama de Pareto – Tipos de defecto
![Diagrama de Pareto](imagenes/panel_vista_previa2.png)

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

```
---

### 📁 Estructura del Proyecto

```
quality-kpi-dashboard/
├── dashboard/
│   └── app.py                  # Código principal del panel
├── data/
│   └── calidad_muestra.csv     # Datos de muestra
├── notebooks/
│   └── analisis_calidad.py     # Análisis exploratorio
├── imagenes/
│   └── panel_vista_previa.png  # Captura del dashboard
├── requisitos.txt              # Dependencias del proyecto
├── .gitignore
└── README.md                   # Este documento
```


---


## 👤 Autor

**David González** – Ingeniero Civil Químico | Data Analytics | Mejora Continua

[![LinkedIn](https://img.shields.io/badge/LinkedIn-David_Gonzalez-blue?style=flat&logo=linkedin)](https://linkedin.com/in/davidgonzalezsz)
[![GitHub](https://img.shields.io/badge/GitHub-icqdgonzalezs-black?style=flat&logo=github)](https://github.com/icqdgonzalezs)

---

*Proyecto desarrollado como parte del portafolio profesional en análisis de datos industriales.*

