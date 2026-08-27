"""Validation rules for the industrial quality dataset."""

from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = [
    "lote",
    "fecha",
    "linea",
    "maquina",
    "turno",
    "operador",
    "unidades_producidas",
    "unidades_defectuosas",
    "unidades_reproceso",
    "unidades_scrap",
    "defecto_tipo",
    "peso_promedio",
    "longitud_promedio",
]


def validar_dataset(df: pd.DataFrame) -> None:
    """Validate the structural and business consistency of the dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset industrial que se desea validar.

    Raises
    ------
    TypeError
        Si el objeto de entrada no es un pandas.DataFrame.

    ValueError
        Si una o más reglas de validación son incumplidas.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("El objeto de entrada debe ser un pandas.DataFrame.")

    errores: list[str] = []

    # 1. Required columns
    columnas_faltantes = [
        col for col in REQUIRED_COLUMNS if col not in df.columns
    ]

    if columnas_faltantes:
        errores.append(
            f"Faltan columnas obligatorias: {', '.join(columnas_faltantes)}"
        )

    # No podemos continuar si faltan columnas necesarias para las
    # validaciones posteriores.
    if errores:
        raise ValueError(" | ".join(errores))

    # 2. Null values
    columnas_con_nulos = df[REQUIRED_COLUMNS].columns[
        df[REQUIRED_COLUMNS].isna().any()
    ].tolist()

    if columnas_con_nulos:
        errores.append(
            f"Existen valores nulos en: {', '.join(columnas_con_nulos)}"
        )

    # 3. Date validity
    fechas = pd.to_datetime(
        df["fecha"],
        format="%Y-%m-%d",
        errors="coerce",
    )

    if fechas.isna().any():
        errores.append("Existen fechas inválidas.")

    # 4. Production volume
    if (df["unidades_producidas"] <= 0).any():
        errores.append("Existen registros con unidades_producidas <= 0.")

    # 5. Defects cannot exceed production
    if (df["unidades_defectuosas"] > df["unidades_producidas"]).any():
        errores.append(
            "Existen registros donde unidades_defectuosas > "
            "unidades_producidas."
        )

    # 6. Loss categories must be non-negative
    if (df["unidades_scrap"] < 0).any():
        errores.append("Existen valores negativos en unidades_scrap.")

    if (df["unidades_reproceso"] < 0).any():
        errores.append("Existen valores negativos en unidades_reproceso.")

    # 7. Defect decomposition must reconcile
    reconciliacion = (
        df["unidades_scrap"] + df["unidades_reproceso"]
        != df["unidades_defectuosas"]
    )

    if reconciliacion.any():
        errores.append(
            "No se cumple: unidades_scrap + unidades_reproceso "
            "= unidades_defectuosas."
        )

    # 8. Continuous process variables must be numeric
    for columna in ("peso_promedio", "longitud_promedio"):
        if not pd.api.types.is_numeric_dtype(df[columna]):
            errores.append(f"{columna} debe ser numérica.")

    # Raise all accumulated validation errors
    if errores:
        raise ValueError(" | ".join(errores))