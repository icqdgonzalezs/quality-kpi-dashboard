# 🎓 Manual de Ejecución y Guía de Replicación
## Quality KPI Dashboard — Panel de Control de Calidad Industrial

**Para:** David Camilo González Santibáñez — Ingeniero Civil Químico, aprendiendo Python aplicado a Data Analytics
**Repositorio:** `github.com/icqdgonzalezs/quality-kpi-dashboard`
**Nivel de este manual:** explicado para quien programa pero aún está construyendo bases sólidas — cada comando y cada concepto se explica antes de usarlo, no se asume que ya lo sabes.

---

# PARTE A — Manual de ejecución

## A.1 Por qué este proyecto necesita Python 3.11 (no el más nuevo)

Antes de tocar un comando, entiende el "por qué", porque es una lección que se repite en cualquier proyecto de Python: **no siempre la versión más nueva es la correcta — la correcta es la compatible con tu entorno.**

Este dashboard usa Streamlit, que internamente depende de una librería llamada `pyarrow` (sirve para manejar tablas de datos de forma eficiente). `pyarrow` se distribuye como **binario precompilado (wheel)** — un archivo ya "cocinado" para una combinación específica de sistema operativo y versión de Python. Si `pip` no encuentra un wheel listo, intenta **compilar desde el código fuente**, y esa compilación puede fallar si tu Mac es antiguo (como macOS Mojave) y no soporta las instrucciones de procesador modernas que el código necesita.

**Conclusión práctica:** en este proyecto, Python 3.11 es obligatorio, no opcional. Python 3.13 (el más reciente) no tiene ningún wheel de `pyarrow` compatible con macOS Mojave — lo verificamos empíricamente, no lo asumimos.

## A.2 Preparar el entorno (cada vez que abres Terminal)

```bash
cd ~/Documents/Industrial-Analytics-Portafolio/01-Quality-KPI-Dashboard
source venv/bin/activate
python3 --version
```

Debe mostrar `Python 3.11.9`. Si por algún motivo muestra 3.13, algo salió mal en la creación del entorno — repara con:

```bash
deactivate
rm -rf venv
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -m venv venv
source venv/bin/activate
```

**Concepto clave — entorno virtual (`venv`):** es una "caja aislada" con su propia copia de Python y sus propias librerías, separada del resto de tu sistema. Sin esto, instalar una librería para un proyecto podría romper otro proyecto que necesita una versión distinta de la misma librería. Es una de las prácticas más importantes que debes internalizar como programador.

Si es la **primera vez** en un computador nuevo:
```bash
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## A.3 Comandos principales, explicados uno por uno

### Generar (o regenerar) el dataset simulado
```bash
python3 src/data_generator.py
```
Esto ejecuta el archivo como **script** (nota el `if __name__ == "__main__":` al final del archivo — es la forma estándar en Python de decir "este código solo corre si ejecuto este archivo directamente, no si lo importo desde otro lado"). Sobrescribe `data/calidad_muestra.csv` con 250 lotes nuevos, usando la misma semilla aleatoria (`seed=42`) — por eso el resultado es **siempre idéntico**, aunque lo corras 100 veces. Esto se llama **reproducibilidad determinística**.

### Correr el dashboard
```bash
streamlit run dashboard/app.py
```
Levanta un servidor web local (por eso ves `Local URL: http://localhost:8501`) y abre tu navegador automáticamente. Streamlit vuelve a ejecutar todo el script `app.py` de arriba a abajo cada vez que interactúas con un filtro — por eso usamos `@st.cache_data` sobre `cargar_datos()`, para no releer el CSV cada vez que mueves el `selectbox`.

Para detenerlo: `Ctrl + C` en la Terminal donde corre.

### Correr los tests
```bash
pytest tests/ -v
```
- `pytest` busca automáticamente archivos que empiecen con `test_` dentro de la carpeta indicada.
- `-v` (verbose) muestra el nombre de cada test individual, no solo un resumen.

Variantes útiles:
```bash
pytest tests/ -v -k "cpk"        # solo tests con "cpk" en el nombre
pytest tests/test_kpis.py -v     # solo un archivo específico
```

### Usar los módulos desde Python directamente (sin Streamlit)
Esto es útil para explorar o depurar sin levantar el dashboard completo:
```bash
python3 -c "
import pandas as pd
from src.kpis import calcular_kpis_globales

df = pd.read_csv('data/calidad_muestra.csv')
print(calcular_kpis_globales(df))
"
```

---

# PARTE B — Arquitectura del proyecto, explicada como clase de programación

Esta sección es la más importante para tu aprendizaje: no solo qué hace cada archivo, sino **por qué está organizado así**, y qué principio de programación aplica.

## B.1 El problema que resuelve la separación en módulos

Antes de la intervención, todo el proyecto era **un solo archivo** (`app.py`) que generaba datos, calculaba KPIs, y dibujaba gráficos, todo mezclado. Esto viola el **Principio de Responsabilidad Única (SRP)**: si mañana quieres cambiar cómo se calcula el Cpk, tendrías que tocar el mismo archivo que dibuja los gráficos — alto riesgo de romper algo que no querías tocar.

La solución fue dividir en capas, cada una con un trabajo específico:

```
src/data_generator.py   -> genera datos (no calcula KPIs, no dibuja nada)
src/kpis.py              -> calcula KPIs descriptivos (no sabe que existe Streamlit)
src/capability.py        -> calcula Cp/Cpk (no sabe que existe Streamlit)
dashboard/app.py         -> orquesta: llama a los modulos de arriba y dibuja
```

**Por qué esto es mejor (y por qué te conviene aprenderlo ahora, temprano):**
1. **Testeable en aislamiento** — puedes probar `calcular_cp_cpk()` con `pytest` sin necesitar abrir un navegador ni levantar Streamlit.
2. **Reutilizable** — si mañana quieres un reporte en Excel en vez de Streamlit, usas los mismos `src/kpis.py` y `src/capability.py` sin tocarlos.
3. **Más fácil de razonar** — cuando lees `capability.py`, sabes que ahí SOLO hay matemática de Cp/Cpk, nada de HTML ni de gráficos.

## B.2 Anatomía de `src/kpis.py` — patrones de Python que debes dominar

```python
def calcular_kpis_globales(df: pd.DataFrame) -> dict:
```

Fíjate en la firma de la función: `df: pd.DataFrame` y `-> dict` son **anotaciones de tipo (type hints)**. No cambian cómo corre el código (Python sigue siendo dinámico), pero le dicen a cualquier persona que lea la función (incluido tú mismo en 3 meses) qué tipo de dato entra y qué tipo sale — y herramientas como tu editor de código las usan para autocompletar y detectar errores antes de ejecutar nada.

```python
def calcular_kpis_por_dimension(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    if dimension not in df.columns:
        raise ValueError(f"Dimension '{dimension}' no existe en el dataset.")
```

Este patrón se llama **validación defensiva (guard clause)**: en vez de dejar que el código falle más adelante con un error críptico de pandas, validamos al entrar a la función y lanzamos un error **claro y específico** con `raise ValueError(...)`. Esto es una práctica profesional — un error que dice "Dimensión 'xyz' no existe" es mucho más útil para depurar que un `KeyError` genérico de pandas 10 líneas después.

```python
agrupado = df.groupby(dimension).agg(
    unidades_producidas=("unidades_producidas", "sum"),
    ...
).reset_index()
```

`groupby().agg()` es el patrón central de pandas para responder preguntas tipo "¿cuál es el total de X, agrupado por Y?" — aquí: "¿cuántas unidades se produjeron, agrupadas por máquina?". El `.reset_index()` al final convierte el resultado agrupado de vuelta en una tabla plana normal (sin él, `dimension` quedaría como índice en vez de columna).

## B.3 Anatomía de `src/capability.py` — manejo de casos límite

```python
def calcular_cp_cpk(valores: pd.Series, lsl: float, usl: float) -> dict:
    valores = valores.dropna()
    n = len(valores)

    if n < 2 or usl <= lsl:
        return {"cp": None, "cpk": None, "clasificacion": "Datos insuficientes"}

    if sigma == 0:
        return {"cp": float("inf"), "cpk": float("inf")}
```

Esto es **programación defensiva ante casos límite (edge cases)**. Antes de hacer el cálculo "feliz" (el caso normal), la función se pregunta: ¿qué pasa si me pasan menos de 2 datos? ¿Qué pasa si LSL es mayor que USL (un error de configuración)? ¿Qué pasa si no hay ninguna variabilidad (sigma=0), lo que causaría una división por cero?

**Esta es exactamente la misma disciplina que evitó el bug del proyecto 1** (el motor de simulación bloqueado): pensar en los casos donde el "camino feliz" no aplica, ANTES de que ese caso aparezca en producción y rompa algo silenciosamente.

## B.4 El patrón de configuración externa (`config/quality_config.yaml`)

```python
with open("config/quality_config.yaml") as f:
    config = yaml.safe_load(f)
```

**Por qué no escribimos los límites LSL/USL directamente en el código Python:** si mañana la especificación del producto cambia (por ejemplo, el peso nominal pasa de 500g a 520g), alguien sin conocimientos de programación podría editar el archivo YAML sin tocar ni entender el código Python. Esto se llama **separación entre configuración y lógica** — un principio que verás repetido en casi cualquier sistema profesional (bases de datos, APIs, aplicaciones web).

---

# PARTE C — Metodología de diagnóstico y remediación aplicada (replicable)

Esto resume, en orden, la disciplina completa que aplicamos — la misma que puedes usar en cualquier proyecto tuyo futuro, propio o heredado de otra persona.

## C.1 Nunca confiar, siempre verificar

No asumimos que `requirements.txt` estaba bien — lo leímos con `cat` y encontramos que tenía instrucciones de `nano` pegadas por error dentro de un comentario, ocultando `streamlit==1.26.0`. No asumimos que Python 3.13 funcionaría — lo probamos empíricamente con `pip install ... --only-binary=:all:` antes de instalar Python 3.11.

## C.2 Diagnóstico de causa raíz, no de síntoma

El error de instalación de `pyarrow` no se resolvió "probando versiones al azar" — se leyó el mensaje de error completo (`SSE4.2 required but compiler doesn't support it`), se entendió que la causa era la combinación Python 3.13 + macOS antiguo, y se atacó esa causa (instalar Python 3.11), no el síntoma superficial (la versión de pyarrow).

## C.3 Detectar afirmaciones no verificadas en la documentación

El README afirmaba `Cpk = 0.85` sin que ese número existiera en ningún cálculo del código. Este tipo de hallazgo — una afirmación falsa y verificable en la documentación — es más grave que un bug técnico, porque afecta la credibilidad de todo el proyecto ante quien lo revise. Se corrigió implementando el cálculo real, no solo borrando la afirmación.

## C.4 Ampliar datos con supuestos documentados, no arbitrarios

Al pasar de 10 a 250 lotes, cada supuesto nuevo (máquina M04 con +1.5 p.p. de defectos, turno Noche con +0.8 p.p.) quedó **documentado en el docstring del generador**, con su justificación (desgaste mecánico, fatiga/supervisión). Un dataset simulado sin supuestos documentados es solo ruido — con ellos, es una narrativa de negocio defendible en una entrevista.

## C.5 Validar resultados contra la lógica de negocio (sanity check)

Después de generar los datos, se verificó explícitamente que el FPY estuviera en un rango realista (94-96%), que M04 apareciera con la peor tasa de defectos, y que el turno Noche apareciera peor que Mañana — confirmando que los patrones diseñados intencionalmente se reflejaban correctamente en los cálculos, antes de construir nada más encima.

## C.6 Prueba de "clona y corre" como criterio de aceptación final

Ningún hallazgo se dio por cerrado hasta clonar el repositorio en una carpeta 100% nueva y correr el flujo completo (`pip install`, `pytest`, `streamlit run`) como lo haría un desconocido — el mismo protocolo aplicado en el proyecto 1.

---

# Glosario rápido para seguir aprendiendo Python

| Término | Qué significa | Dónde lo viste hoy |
|---|---|---|
| **Type hints** | Anotaciones opcionales de tipo de dato (`df: pd.DataFrame`) | Firmas de funciones en `kpis.py` |
| **Guard clause** | Validar condiciones al inicio de una función y salir temprano si algo está mal | `if dimension not in df.columns: raise ValueError(...)` |
| **Edge case** | Caso límite o poco común que puede romper el "camino feliz" del código | `sigma == 0`, `n < 2` en `capability.py` |
| **`groupby().agg()`** | Patrón de pandas para agregar datos por categoría | `calcular_kpis_por_dimension()` |
| **`@st.cache_data`** | Decorador de Streamlit que evita recalcular algo costoso en cada interacción | `cargar_datos()` en `app.py` |
| **Reproducibilidad determinística** | Mismo código + misma semilla = mismo resultado, siempre | `np.random.default_rng(seed=42)` |
| **Configuración externa** | Separar parámetros ajustables del código fuente | `config/quality_config.yaml` |
| **SRP (Single Responsibility Principle)** | Cada módulo/función debe tener una sola razón para cambiar | División en `data_generator.py` / `kpis.py` / `capability.py` |

---

**Manual preparado como guía de referencia permanente para el portafolio de Data Analytics Industrial de David Camilo González Santibáñez.**
