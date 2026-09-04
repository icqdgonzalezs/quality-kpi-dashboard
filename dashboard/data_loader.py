from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "calidad_muestra.csv"
QUALITY_CONFIG_PATH = PROJECT_ROOT / "config" / "quality_config.yaml"


def cargar_datos() -> tuple[pd.DataFrame, dict]:
    """Carga dataset y configuración analítica para la aplicación Dash."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"No existe el dataset: {DATA_PATH}")

    if not QUALITY_CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"No existe la configuración: {QUALITY_CONFIG_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    if "fecha" in df.columns:
        df["fecha"] = pd.to_datetime(
            df["fecha"],
            errors="coerce",
            format="mixed",
        )

    with QUALITY_CONFIG_PATH.open(encoding="utf-8") as archivo:
        config = yaml.safe_load(archivo)

    if config is None:
        config = {}

    return df, config
