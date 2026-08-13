"""
Generador de dataset simulado de calidad industrial.

SUPUESTOS DOCUMENTADOS (metodología):
- 2 líneas de producción (Línea 1, Línea 2), 2 máquinas por línea (4 total).
- 3 turnos: Mañana, Tarde, Noche. El turno Noche tiene una tasa de defecto
  base ligeramente mayor (+0.8 p.p.), reflejando el efecto de fatiga/menor
  supervisión reportado en la literatura de gestión de calidad.
- La máquina "M04" tiene una tasa de defecto base mayor a las demás
  (+1.5 p.p.), simulando desgaste mecánico progresivo — es el cuello de
  botella de calidad intencional del dataset.
- De las unidades defectuosas, 70% son recuperables mediante reproceso
  y 30% son scrap irrecuperable (supuesto fijo, documentado aquí).
- peso_promedio y longitud_promedio son variables continuas con
  distribución normal, usadas para el cálculo de Cp/Cpk. Los límites de
  especificación (LSL/USL) están definidos en config/quality_config.yaml.
- Semilla aleatoria fija (random_seed=42) para reproducibilidad total.
"""
import numpy as np
import pandas as pd

RANDOM_SEED = 42
N_LOTES = 250
FECHA_INICIO = "2025-01-01"

LINEAS = {
    "Línea 1": ["M01", "M02"],
    "Línea 2": ["M03", "M04"],  # M04 = máquina con mayor desgaste simulado
}
TURNOS = ["Mañana", "Tarde", "Noche"]
OPERADORES = ["Operador A", "Operador B", "Operador C",
              "Operador D", "Operador E", "Operador F"]
TIPOS_DEFECTO = ["Mancha", "Rayadura", "Peso fuera de rango",
                  "Largo fuera de rango", "Contaminación"]
PROB_DEFECTO_TIPO = [0.35, 0.25, 0.20, 0.15, 0.05]  # distribución tipo Pareto

# Especificaciones de proceso (usadas también en config/quality_config.yaml)
PESO_NOMINAL, PESO_STD, PESO_LSL, PESO_USL = 500.0, 2.5, 492.0, 508.0
LARGO_NOMINAL, LARGO_STD, LARGO_LSL, LARGO_USL = 120.0, 0.8, 117.5, 122.5


def _tasa_defecto_base(maquina: str, turno: str) -> float:
    """Tasa de defecto base (%) según máquina y turno, con los supuestos
    documentados en el docstring del módulo."""
    tasa = 3.8  # tasa base de línea, en %
    if maquina == "M04":
        tasa += 1.5
    if turno == "Noche":
        tasa += 0.8
    return tasa


def generar_dataset(n_lotes: int = N_LOTES, seed: int = RANDOM_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    fechas = pd.date_range(start=FECHA_INICIO, periods=n_lotes, freq="D")

    registros = []
    for i, fecha in enumerate(fechas):
        linea = rng.choice(list(LINEAS.keys()))
        maquina = rng.choice(LINEAS[linea])
        turno = rng.choice(TURNOS)
        operador = rng.choice(OPERADORES)

        unidades_producidas = int(rng.normal(1000, 40))
        tasa_defecto = _tasa_defecto_base(maquina, turno) / 100.0
        unidades_defectuosas = int(rng.binomial(unidades_producidas, tasa_defecto))

        # División reproceso (recuperable) vs scrap (irrecuperable)
        unidades_scrap = int(rng.binomial(unidades_defectuosas, 0.30))
        unidades_reproceso = unidades_defectuosas - unidades_scrap

        defecto_tipo = rng.choice(TIPOS_DEFECTO, p=PROB_DEFECTO_TIPO)

        # Variables continuas para Cp/Cpk — con leve corrimiento en Línea 2
        corrimiento_peso = -0.6 if linea == "Línea 2" else 0.0
        peso_promedio = round(rng.normal(PESO_NOMINAL + corrimiento_peso, PESO_STD), 2)
        longitud_promedio = round(rng.normal(LARGO_NOMINAL, LARGO_STD), 2)

        registros.append({
            "lote": f"L{i+1:04d}",
            "fecha": fecha.strftime("%Y-%m-%d"),
            "linea": linea,
            "maquina": maquina,
            "turno": turno,
            "operador": operador,
            "unidades_producidas": unidades_producidas,
            "unidades_defectuosas": unidades_defectuosas,
            "unidades_reproceso": unidades_reproceso,
            "unidades_scrap": unidades_scrap,
            "defecto_tipo": defecto_tipo,
            "peso_promedio": peso_promedio,
            "longitud_promedio": longitud_promedio,
        })

    return pd.DataFrame(registros)


if __name__ == "__main__":
    df = generar_dataset()
    df.to_csv("data/calidad_muestra.csv", index=False)
    print(f"Dataset generado: {len(df)} lotes → data/calidad_muestra.csv")
    print(df.head())
