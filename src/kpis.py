"""
Cálculo de KPIs descriptivos de calidad industrial.

Definiciones (según terminología estándar de manufactura):
- FPY (First Pass Yield): % de unidades que salen conformes a la primera,
  sin necesidad de reproceso. FPY = (producidas - defectuosas) / producidas.
- Tasa de scrap: % de unidades producidas que se pierden de forma
  irrecuperable (no reprocesables).
- Tasa de reproceso: % de unidades que requieren reproceso para ser
  recuperadas como conformes.
- Tasa de defectos: % de unidades producidas que resultaron defectuosas
  (scrap + reproceso combinados).
"""
import pandas as pd


def calcular_kpis_globales(df: pd.DataFrame) -> dict:
    """Calcula los KPIs agregados sobre el dataset completo (todas las líneas/turnos)."""
    total_producidas = df["unidades_producidas"].sum()
    total_defectuosas = df["unidades_defectuosas"].sum()
    total_scrap = df["unidades_scrap"].sum()
    total_reproceso = df["unidades_reproceso"].sum()

    return {
        "fpy": (total_producidas - total_defectuosas) / total_producidas,
        "tasa_defectos": total_defectuosas / total_producidas,
        "tasa_scrap": total_scrap / total_producidas,
        "tasa_reproceso": total_reproceso / total_producidas,
        "total_producidas": int(total_producidas),
        "total_defectuosas": int(total_defectuosas),
        "total_scrap": int(total_scrap),
        "total_reproceso": int(total_reproceso),
    }


def calcular_kpis_por_dimension(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """Calcula FPY y tasa de defectos agrupado por una dimensión
    (ej. 'linea', 'turno', 'maquina', 'operador'). Permite responder
    preguntas como '¿qué turno tiene peor desempeño de calidad?'."""
    if dimension not in df.columns:
        raise ValueError(f"Dimensión '{dimension}' no existe en el dataset.")

    agrupado = df.groupby(dimension).agg(
        unidades_producidas=("unidades_producidas", "sum"),
        unidades_defectuosas=("unidades_defectuosas", "sum"),
        unidades_scrap=("unidades_scrap", "sum"),
        unidades_reproceso=("unidades_reproceso", "sum"),
        n_lotes=("lote", "count"),
    ).reset_index()

    agrupado["fpy"] = (
        (agrupado["unidades_producidas"] - agrupado["unidades_defectuosas"])
        / agrupado["unidades_producidas"]
    )
    agrupado["tasa_defectos"] = agrupado["unidades_defectuosas"] / agrupado["unidades_producidas"]
    return agrupado.sort_values("tasa_defectos", ascending=False)


def calcular_pareto(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla de Pareto: frecuencia y porcentaje acumulado por tipo de defecto."""
    pareto = df["defecto_tipo"].value_counts().reset_index()
    pareto.columns = ["defecto", "frecuencia"]
    pareto["porcentaje"] = pareto["frecuencia"] / pareto["frecuencia"].sum() * 100
    pareto["porcentaje_acumulado"] = pareto["porcentaje"].cumsum()
    return pareto


def identificar_lote_critico(df: pd.DataFrame) -> pd.Series:
    """Retorna el lote con mayor tasa de defectos (no solo mayor conteo absoluto,
    para no sesgar hacia lotes con mayor volumen de producción)."""
    df = df.copy()
    df["tasa_defectos_lote"] = df["unidades_defectuosas"] / df["unidades_producidas"]
    return df.loc[df["tasa_defectos_lote"].idxmax()]
