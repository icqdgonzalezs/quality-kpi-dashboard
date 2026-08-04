cat > README.md << 'EOF'
# 📊 Quality KPI Dashboard

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.26.0-red?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**Panel interactivo de monitoreo de calidad para líneas de producción.**  
Simula una línea real, calcula indicadores de defectos, capacidad de proceso (Cp/Cpk) y genera diagramas de Pareto, facilitando la toma de decisiones basada en datos.

---

## ✨ Características principales

- **Simulación de datos realista** para una línea de producción.
- **Métricas de calidad** en tiempo simulado: tasa de defectos, defectos totales, lote crítico.
- **Análisis de capacidad de proceso** (Cp y Cpk).
- **Diagrama de Pareto** interactivo con identificación del principio 80/20.
- **Visualización temporal** de la evolución de defectos.
- **Exportación y uso de datos locales** en formato CSV.

---

## 📈 KPIs implementados

| Indicador | Descripción |
|-----------|-------------|
| **Tasa de defectos (%)** | Porcentaje de unidades defectuosas por lote |
| **Total defectuosos** | Conteo absoluto de unidades con defectos |
| **Lote crítico** | Lote con el mayor número de defectos |
| **Diagrama de Pareto** | Frecuencia de defectos por tipo (80/20) |
| **Evolución temporal** | Tendencia de la tasa de defectos a lo largo del tiempo |

---

## 🛠️ Stack tecnológico

| Herramienta | Uso |
|-------------|-----|
| **Python 3.9+** | Lenguaje base |
| **Streamlit** | Framework para dashboard interactivo |
| **Plotly Express** | Gráficos interactivos (líneas, barras, Pareto) |
| **Pandas** | Manipulación y análisis de datos |
| **NumPy** | Cálculos numéricos y generación de datos simulados |

---

## 📸 Capturas del panel

**Evolución de la tasa de defectos**  
![Evolución de la tasa de defectos](imagenes/panel_vista_previa1.png)

**Diagrama de Pareto – Tipos de defecto**  
![Diagrama de Pareto](imagenes/panel_vista_previa2.png)

---

## ⚙️ Instalación y ejecución

```bash
# Clonar el repositorio
git clone https://github.com/icqdgonzalezs/quality-kpi-dashboard.git
cd quality-kpi-dashboard

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el panel
streamlit run dashboard/app.py

```
---

### 📁 Estructura del Proyecto

```
quality-kpi-dashboard/
├── dashboard/
│   └── app.py                  # Aplicación principal de Streamlit
├── data/
│   └── calidad_muestra.csv     # Datos de muestra (simulados)
├── imagenes/
│   ├── panel_vista_previa1.png # Captura de evolución temporal
│   └── panel_vista_previa2.png # Captura del diagrama de Pareto
├── notebooks/
│   └── analisis_calidad.py     # Análisis exploratorio de los datos
├── requirements.txt            # Dependencias del proyecto
├── .gitignore
└── README.md                   # Este documento
```


---


## 👤 Autor

**David González** – Ingeniero Civil Químico | Data Analytics | Mejora Continua  
✉️ [icq.dgonzalezs@gmail.com](mailto:icq.dgonzalezs@gmail.com)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-David_González-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/davidgonzalezsz)
[![GitHub](https://img.shields.io/badge/GitHub-icqdgonzalezs-181717?style=flat&logo=github&logoColor=white)](https://github.com/icqdgonzalezs)
[![Email](https://img.shields.io/badge/Email-icq.dgonzalezs%40gmail.com-EA4335?style=flat&logo=gmail&logoColor=white)](mailto:icq.dgonzalezs@gmail.com)

---

*Proyecto desarrollado como parte del portafolio profesional en análisis de datos industriales.*



Proyecto desarrollado como parte del portafolio profesional en análisis de datos industriales.



