"""
Generador de datos sintéticos industriales para Manufacturing Analytics.

Genera un conjunto de datos de producción y defectos para una planta ficticia
de 4 líneas y 23 equipos, con estructura realista, eventos de desviación,
variabilidad por turno y reproducibilidad garantizada (semilla fija 42).

Los datos generados se guardan en data/raw/synthetic_production_data.csv

Autor: Sistema Industrial KPI Intelligence
Fecha: 2025-XX-XX
"""

import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import yaml

# ----------------------------------------------------------------------
# Configuración
# ----------------------------------------------------------------------

def load_generator_config() -> dict:
    """Carga la configuración del generador desde YAML."""
    config_path = Path(__file__).resolve().parent.parent / "config" / "generator_config.yaml"
    with config_path.open(encoding="utf-8") as file:
        return yaml.safe_load(file)


GENERATOR_CONFIG = load_generator_config()

RANDOM_SEED = int(GENERATOR_CONFIG["generation"]["random_seed"])
START_DATE = datetime.strptime(GENERATOR_CONFIG["generation"]["start_date"], "%Y-%m-%d")
END_DATE = datetime.strptime(GENERATOR_CONFIG["generation"]["end_date"], "%Y-%m-%d")

BASE_PRODUCTION = GENERATOR_CONFIG["production_per_shift"]
BASE_DEFECT_RATE = GENERATOR_CONFIG["base_defect_rate_pct"]
DEFECT_TYPE_DIST = {
    equipment_type: {"Sin defecto": max(0.0, 1.0 - sum(distribution.values())), **distribution}
    for equipment_type, distribution in GENERATOR_CONFIG["defect_type_distribution"].items()
}
DRIFT_EVENTS = GENERATOR_CONFIG["drift_events"]
PRODUCT_EFFECT = {
    (item["equipment_id"], item["product_id"]): item["factor"]
    for item in GENERATOR_CONFIG["product_effect"]
}


def load_plant_config() -> dict:
    """Carga la configuración maestra de planta desde YAML."""
    config_path = Path(__file__).resolve().parent.parent / "config" / "plant_config.yaml"
    with config_path.open(encoding="utf-8") as file:
        return yaml.safe_load(file)


def create_equipment_master() -> pd.DataFrame:
    """Crea el maestro de equipos desde plant_config.yaml."""
    config = load_plant_config()

    rows = []
    for line_id, line_info in config["lines"].items():
        for equipment in line_info["equipment"]:
            rows.append({
                "line_id": line_id,
                "line_name": line_info["name"],
                "equipment_id": equipment["id"],
                "equipment_type": equipment["type"],
                "equipment_name": equipment["name"],
                "is_critical": equipment["critical"],
                "products": [
                    product_id
                    for product_id, product in config["products"].items()
                    if line_id in product["lines"]
                ],
            })

    return pd.DataFrame(rows)

def generate_working_dates(start: datetime, end: datetime) -> list:
    """
    Genera lista de fechas laborables (lunes a viernes) entre start y end.
    """
    dates = []
    current = start
    while current <= end:
        if current.weekday() < 5:  # 0=lunes, 4=viernes
            dates.append(current)
        current += timedelta(days=1)
    return dates

def assign_operator(
    shift: str,
    rng: np.random.Generator,
    operators: list[str],
) -> str:
    """Asigna un operador utilizando la configuración externa."""
    if shift == "Noche":
        operator_pool = operators[16:24]
    else:
        operator_pool = operators[:16]

    return rng.choice(operator_pool)

def get_defect_rate(equipment_id: str, equipment_type: str, date: datetime,
                    shift: str, product_id: str) -> float:
    """
    Calcula la tasa de defectos para un equipo en una fecha y turno dados,
    aplicando eventos de drift, efecto de turno y producto.
    """
    base_rate = BASE_DEFECT_RATE.get(equipment_type, 1.0) / 100.0

    # Ajuste por turno: noche más variable
    if shift == "Noche":
        base_rate *= 1.3
    elif shift == "Tarde":
        base_rate *= 1.1

    # Aplicar drift events
    for event in DRIFT_EVENTS:
        if event["equipment_id"] == equipment_id:
            if event["start_month"] <= date.month <= event["end_month"]:
                progress = (date.month - event["start_month"]) / (
                    event["end_month"] - event["start_month"] + 1
                )
                factor = 1.0 + progress * (event["factor_increment"] - 1.0)
                base_rate *= factor

    # Efecto específico del producto
    product_key = (equipment_id, product_id)
    if product_key in PRODUCT_EFFECT:
        base_rate *= PRODUCT_EFFECT[product_key]

    # Limitar entre 0 y 0.5
    return min(max(base_rate, 0.0001), 0.5)

def generate_production_data() -> pd.DataFrame:
    """
    Genera el dataset completo de producción y defectos.
    """
    rng = np.random.default_rng(RANDOM_SEED)

    config = load_plant_config()
    shifts = config["shifts"]
    operators = config["operators"]["ids"]
    equipment_master = create_equipment_master()
    working_days = generate_working_dates(START_DATE, END_DATE)

    records = []
    for _, eq_row in equipment_master.iterrows():
        line_id = eq_row["line_id"]
        equipment_id = eq_row["equipment_id"]
        equipment_type = eq_row["equipment_type"]
        products = eq_row["products"]

        for date in working_days:
            for shift in shifts:
                # Elegir producto aleatorio de la línea
                product_id = rng.choice(products)

                # Producción base con factor de turno
                base_prod = BASE_PRODUCTION.get(equipment_type, 3000)
                if shift == "Noche":
                    prod_factor = rng.normal(0.93, 0.05)
                elif shift == "Tarde":
                    prod_factor = rng.normal(0.98, 0.03)
                else:
                    prod_factor = rng.normal(1.0, 0.02)
                prod_factor = max(0.5, min(1.2, prod_factor))  # clamp

                units_produced = int(round(base_prod * prod_factor))

                # Tasa de defectos
                defect_rate = get_defect_rate(equipment_id, equipment_type, date, shift, product_id)

                # Generar unidades defectuosas usando distribución binomial
                units_defective = rng.binomial(units_produced, defect_rate)

                # Dividir entre scrap y rework
                scrap_ratio = rng.beta(2, 3)  # media ~0.4
                units_scrap = int(round(units_defective * scrap_ratio))
                units_rework = units_defective - units_scrap

                # Seleccionar defect_type según distribución del equipo
                defect_types = list(DEFECT_TYPE_DIST[equipment_type].keys())
                probs = list(DEFECT_TYPE_DIST[equipment_type].values())
                # Normalizar por si no suma 1
                probs = np.array(probs) / sum(probs)
                if units_defective > 0:
                    defect_type = rng.choice(defect_types, p=probs)
                else:
                    defect_type = "Sin defecto"

                # Timestamp del turno: se asigna una hora del turno
                hour_map = {"Mañana": 9, "Tarde": 15, "Noche": 23}
                timestamp = datetime(date.year, date.month, date.day, hour_map[shift])

                operator_id = assign_operator(shift, rng, operators)

                records.append({
                    "timestamp": timestamp,
                    "date": date.strftime("%Y-%m-%d"),
                    "year": date.year,
                    "month": date.month,
                    "week": date.isocalendar()[1],
                    "shift": shift,
                    "operator_id": operator_id,
                    "line_id": line_id,
                    "equipment_id": equipment_id,
                    "equipment_type": equipment_type,
                    "product_id": product_id,
                    "units_produced": units_produced,
                    "units_defective": units_defective,
                    "units_scrap": units_scrap,
                    "units_rework": units_rework,
                    "defect_type": defect_type,
                })

    df = pd.DataFrame(records)
    df = df.sort_values(["timestamp", "line_id", "equipment_id"]).reset_index(drop=True)
    return df

def main():
    """
    Función principal: genera los datos y los guarda en CSV.
    """
    print("Generando datos sintéticos...")
    df = generate_production_data()

    # Crear directorio si no existe
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "synthetic_production_data.csv"

    df.to_csv(output_path, index=False)
    print(f"Dataset guardado en {output_path}")
    print(f"Total de registros: {len(df)}")
    print("\nPrimeras 5 filas:")
    print(df.head())
    print("\nResumen de defectos por equipo:")
    print(df.groupby("equipment_id")["units_defective"].sum().sort_values(ascending=False).head(10))

if __name__ == "__main__":
    main()
