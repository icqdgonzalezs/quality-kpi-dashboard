from __future__ import annotations

import pandas as pd

from src.kpis import calcular_kpis_por_dimension


def calcular_estado_equipo(
    tasa: float,
    promedio: float,
    desviacion: float,
) -> str:
    """Clasifica el desempeño relativo de un equipo."""
    if desviacion == 0:
        return "NORMAL" if tasa <= promedio else "WATCH"

    limite_watch = promedio + (0.5 * desviacion)
    limite_priority = promedio + desviacion

    if tasa <= limite_watch:
        return "NORMAL"

    if tasa <= limite_priority:
        return "WATCH"

    return "PRIORITY"


def construir_ranking_equipos(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Construye el ranking analítico de desempeño por equipo."""
    if df.empty:
        return pd.DataFrame()

    return calcular_kpis_por_dimension(
        df,
        "equipo",
    )
