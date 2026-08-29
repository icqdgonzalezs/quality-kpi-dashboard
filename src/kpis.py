"""
Cálculo de KPIs descriptivos de calidad industrial.

Este módulo contiene únicamente lógica analítica.
La presentación de resultados se realiza en Streamlit.

Principio de diseño:
- validation.py protege la calidad del dataset.
- kpis.py protege la integridad de los cálculos.
- dashboard/app.py presenta los resultados.
"""

from __future__ import annotations

import pandas as pd


# ---------------------------------------------------------------------
# CONFIGURACIÓN ANALÍTICA
# ---------------------------------------------------------------------

COLUMNAS_KPI = [
    "lote",
    "unidades_producidas",
    "unidades_defectuosas",
    "unidades_scrap",
    "unidades_reproceso",
]

COLUMNAS_PARETO = [
    "defecto_tipo",
    "unidades_defectuosas",
]

DIMENSIONES_OPERACIONALES = [
    "linea",
    "maquina",
    "equipo",
    "turno",
    "operador",
]


# ---------------------------------------------------------------------
# VALIDACIÓN INTERNA DEL MOTOR KPI
# ---------------------------------------------------------------------

def _validar_dataframe(
    df: pd.DataFrame,
) -> None:
    """Valida que la entrada sea un DataFrame no vacío."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "El objeto de entrada debe ser un pandas.DataFrame."
        )

    if df.empty:
        raise ValueError(
            "El dataset no puede estar vacío."
        )


def _validar_columnas(
    df: pd.DataFrame,
    columnas: list[str],
) -> None:
    """Valida columnas necesarias para un cálculo."""
    _validar_dataframe(df)

    faltantes = [
        columna
        for columna in columnas
        if columna not in df.columns
    ]

    if faltantes:
        raise ValueError(
            "Faltan columnas requeridas: "
            + ", ".join(faltantes)
        )


def _validar_integridad_operacional(
    df: pd.DataFrame,
) -> None:
    """Valida relaciones básicas necesarias para calcular KPIs."""
    columnas = [
        "unidades_producidas",
        "unidades_defectuosas",
        "unidades_scrap",
        "unidades_reproceso",
    ]

    _validar_columnas(df, columnas)

    if not df[columnas].apply(
        lambda serie: pd.api.types.is_numeric_dtype(serie)
    ).all():
        raise ValueError(
            "Las columnas de unidades deben ser numéricas."
        )

    if df[columnas].isna().any().any():
        raise ValueError(
            "Las columnas de unidades no pueden contener valores nulos."
        )

    if (df["unidades_producidas"] <= 0).any():
        raise ValueError(
            "Todas las unidades producidas deben ser mayores que cero."
        )

    if (df["unidades_defectuosas"] < 0).any():
        raise ValueError(
            "Las unidades defectuosas no pueden ser negativas."
        )

    if (
        df["unidades_defectuosas"]
        > df["unidades_producidas"]
    ).any():
        raise ValueError(
            "Las unidades defectuosas no pueden superar "
            "las unidades producidas."
        )

    if (df["unidades_scrap"] < 0).any():
        raise ValueError(
            "Las unidades de scrap no pueden ser negativas."
        )

    if (df["unidades_reproceso"] < 0).any():
        raise ValueError(
            "Las unidades de reproceso no pueden ser negativas."
        )

    reconciliacion = (
        df["unidades_scrap"]
        + df["unidades_reproceso"]
        == df["unidades_defectuosas"]
    )

    if not reconciliacion.all():
        raise ValueError(
            "Scrap + reproceso debe coincidir "
            "con unidades defectuosas."
        )


# ---------------------------------------------------------------------
# KPI GLOBALES
# ---------------------------------------------------------------------

def calcular_kpis_globales(
    df: pd.DataFrame,
) -> dict:
    """Calcula KPIs agregados sobre todo el dataset.

    Las tasas utilizan unidades totales como denominador.
    Esto evita el sesgo de promediar tasas lote a lote.
    """
    _validar_columnas(
        df,
        COLUMNAS_KPI,
    )

    _validar_integridad_operacional(df)

    total_producidas = df[
        "unidades_producidas"
    ].sum()

    total_defectuosas = df[
        "unidades_defectuosas"
    ].sum()

    total_scrap = df[
        "unidades_scrap"
    ].sum()

    total_reproceso = df[
        "unidades_reproceso"
    ].sum()

    return {
        "fpy": (
            total_producidas
            - total_defectuosas
        )
        / total_producidas,
        "tasa_defectos": (
            total_defectuosas
            / total_producidas
        ),
        "tasa_scrap": (
            total_scrap
            / total_producidas
        ),
        "tasa_reproceso": (
            total_reproceso
            / total_producidas
        ),
        "total_producidas": int(
            total_producidas
        ),
        "total_defectuosas": int(
            total_defectuosas
        ),
        "total_scrap": int(
            total_scrap
        ),
        "total_reproceso": int(
            total_reproceso
        ),
    }


# ---------------------------------------------------------------------
# KPI POR DIMENSIÓN
# ---------------------------------------------------------------------

def calcular_kpis_por_dimension(
    df: pd.DataFrame,
    dimension: str,
) -> pd.DataFrame:
    """Calcula KPIs agregados por dimensión operacional.

    Dimensiones soportadas:
    - linea
    - maquina
    - equipo
    - turno
    - operador

    ``equipo`` representa un equipo físico único y evita
    mezclar M01 de Línea 1 con M01 de Línea 2.
    """
    _validar_columnas(
        df,
        COLUMNAS_KPI,
    )

    _validar_integridad_operacional(df)

    if dimension not in DIMENSIONES_OPERACIONALES:
        raise ValueError(
            f"Dimensión '{dimension}' no es válida. "
            f"Use una de: {', '.join(DIMENSIONES_OPERACIONALES)}."
        )

    if dimension not in df.columns:
        raise ValueError(
            f"Dimensión '{dimension}' no existe en el dataset."
        )

    agrupado = (
        df.groupby(
            dimension,
            dropna=False,
        )
        .agg(
            unidades_producidas=(
                "unidades_producidas",
                "sum",
            ),
            unidades_defectuosas=(
                "unidades_defectuosas",
                "sum",
            ),
            unidades_scrap=(
                "unidades_scrap",
                "sum",
            ),
            unidades_reproceso=(
                "unidades_reproceso",
                "sum",
            ),
            n_lotes=(
                "lote",
                "count",
            ),
        )
        .reset_index()
    )

    agrupado["fpy"] = (
        agrupado["unidades_producidas"]
        - agrupado["unidades_defectuosas"]
    ) / agrupado["unidades_producidas"]

    agrupado["tasa_defectos"] = (
        agrupado["unidades_defectuosas"]
        / agrupado["unidades_producidas"]
    )

    agrupado["tasa_scrap"] = (
        agrupado["unidades_scrap"]
        / agrupado["unidades_producidas"]
    )

    agrupado["tasa_reproceso"] = (
        agrupado["unidades_reproceso"]
        / agrupado["unidades_producidas"]
    )

    return (
        agrupado
        .sort_values(
            "tasa_defectos",
            ascending=False,
        )
        .reset_index(drop=True)
    )


# ---------------------------------------------------------------------
# PARETO
# ---------------------------------------------------------------------

def calcular_pareto(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Calcula Pareto de defectos por unidades defectuosas."""
    _validar_columnas(
        df,
        COLUMNAS_PARETO,
    )

    if not pd.api.types.is_numeric_dtype(
        df["unidades_defectuosas"]
    ):
        raise ValueError(
            "unidades_defectuosas debe ser numérica."
        )

    if df["unidades_defectuosas"].isna().any():
        raise ValueError(
            "unidades_defectuosas no puede contener nulos."
        )

    if (df["unidades_defectuosas"] < 0).any():
        raise ValueError(
            "unidades_defectuosas no puede ser negativa."
        )

    pareto = (
        df.groupby(
            "defecto_tipo",
            dropna=False,
        )["unidades_defectuosas"]
        .sum()
        .reset_index()
        .rename(
            columns={
                "defecto_tipo": "defecto",
                "unidades_defectuosas": "frecuencia",
            }
        )
        .sort_values(
            "frecuencia",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    total_defectuosas = pareto[
        "frecuencia"
    ].sum()

    # Un dataset puede ser válido y no tener defectos.
    # En ese caso devolvemos una tabla vacía en lugar
    # de lanzar una excepción.
    if total_defectuosas == 0:
        return pd.DataFrame(
            columns=[
                "defecto",
                "frecuencia",
                "porcentaje",
                "porcentaje_acumulado",
            ]
        )

    pareto["porcentaje"] = (
        pareto["frecuencia"]
        / total_defectuosas
        * 100
    )

    pareto[
        "porcentaje_acumulado"
    ] = pareto["porcentaje"].cumsum()

    return pareto


# ---------------------------------------------------------------------
# LOTE CRÍTICO
# ---------------------------------------------------------------------

def identificar_lote_critico(
    df: pd.DataFrame,
) -> pd.Series:
    """Retorna el lote con mayor tasa de defectos."""
    columnas = [
        "lote",
        "unidades_producidas",
        "unidades_defectuosas",
    ]

    _validar_columnas(
        df,
        columnas,
    )

    if not pd.api.types.is_numeric_dtype(
        df["unidades_producidas"]
    ):
        raise ValueError(
            "unidades_producidas debe ser numérica."
        )

    if not pd.api.types.is_numeric_dtype(
        df["unidades_defectuosas"]
    ):
        raise ValueError(
            "unidades_defectuosas debe ser numérica."
        )

    if df[
        [
            "unidades_producidas",
            "unidades_defectuosas",
        ]
    ].isna().any().any():
        raise ValueError(
            "Las unidades utilizadas para "
            "calcular el lote crítico no pueden contener nulos."
        )

    if (
        df["unidades_producidas"]
        <= 0
    ).any():
        raise ValueError(
            "Todas las unidades producidas "
            "deben ser mayores que cero."
        )

    if (
        df["unidades_defectuosas"]
        < 0
    ).any():
        raise ValueError(
            "Las unidades defectuosas "
            "no pueden ser negativas."
        )

    if (
        df["unidades_defectuosas"]
        > df["unidades_producidas"]
    ).any():
        raise ValueError(
            "Las unidades defectuosas "
            "no pueden superar las producidas."
        )

    datos = df.copy()

    datos["tasa_defectos_lote"] = (
        datos["unidades_defectuosas"]
        / datos["unidades_producidas"]
    )

    return datos.loc[
        datos["tasa_defectos_lote"].idxmax()
    ]