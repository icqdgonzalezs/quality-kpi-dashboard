"""Validation and data-quality rules for the industrial dataset."""

from __future__ import annotations

from typing import Any

import pandas as pd


REQUIRED_COLUMNS = [
    "lote",
    "fecha",
    "linea",
    "maquina",
    "equipo",
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

NUMERIC_COLUMNS = [
    "unidades_producidas",
    "unidades_defectuosas",
    "unidades_reproceso",
    "unidades_scrap",
    "peso_promedio",
    "longitud_promedio",
]

CONTINUOUS_COLUMNS = [
    "peso_promedio",
    "longitud_promedio",
]


def _validar_tipo(df: pd.DataFrame) -> list[str]:
    """Valida que la entrada corresponda a un DataFrame."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "El objeto de entrada debe ser un pandas.DataFrame."
        )
    return []


def _obtener_columnas_faltantes(
    df: pd.DataFrame,
) -> list[str]:
    """Devuelve las columnas obligatorias que no existen."""
    return [
        columna
        for columna in REQUIRED_COLUMNS
        if columna not in df.columns
    ]


def _validar_columnas_obligatorias(
    df: pd.DataFrame,
) -> list[str]:
    """Valida la existencia de todas las columnas requeridas."""
    columnas_faltantes = _obtener_columnas_faltantes(df)

    if columnas_faltantes:
        return [
            "Faltan columnas obligatorias: "
            + ", ".join(columnas_faltantes)
        ]

    return []


def _validar_nulos(
    df: pd.DataFrame,
) -> list[str]:
    """Detecta valores nulos en columnas obligatorias."""
    columnas_con_nulos = (
        df[REQUIRED_COLUMNS]
        .columns[
            df[REQUIRED_COLUMNS].isna().any()
        ]
        .tolist()
    )

    if columnas_con_nulos:
        return [
            "Existen valores nulos en: "
            + ", ".join(columnas_con_nulos)
        ]

    return []


def _validar_fechas(
    df: pd.DataFrame,
) -> list[str]:
    """Valida fechas con formato YYYY-MM-DD."""
    fechas = pd.to_datetime(
        df["fecha"],
        format="%Y-%m-%d",
        errors="coerce",
    )

    if fechas.isna().any():
        return ["Existen fechas inválidas."]

    return []


def _validar_produccion(
    df: pd.DataFrame,
) -> list[str]:
    """Valida reglas asociadas al volumen producido."""
    errores: list[str] = []

    if (df["unidades_producidas"] <= 0).any():
        errores.append(
            "Existen registros con "
            "unidades_producidas <= 0."
        )

    if (
        df["unidades_defectuosas"]
        > df["unidades_producidas"]
    ).any():
        errores.append(
            "Existen registros donde "
            "unidades_defectuosas > "
            "unidades_producidas."
        )

    return errores


def _validar_perdidas(
    df: pd.DataFrame,
) -> list[str]:
    """Valida scrap, reproceso y conciliación."""
    errores: list[str] = []

    if (df["unidades_scrap"] < 0).any():
        errores.append(
            "Existen valores negativos en unidades_scrap."
        )

    if (df["unidades_reproceso"] < 0).any():
        errores.append(
            "Existen valores negativos en "
            "unidades_reproceso."
        )

    reconciliacion = (
        df["unidades_scrap"]
        + df["unidades_reproceso"]
        != df["unidades_defectuosas"]
    )

    if reconciliacion.any():
        errores.append(
            "No se cumple: unidades_scrap + "
            "unidades_reproceso = "
            "unidades_defectuosas."
        )

    return errores


def _validar_equipo(
    df: pd.DataFrame,
) -> list[str]:
    """Valida la identidad compuesta línea + máquina."""
    esperado = (
        df["linea"]
        .astype(str)
        .str.extract(r"(\d+)", expand=False)
        .map(lambda numero: f"L{numero}")
        + "-"
        + df["maquina"].astype(str)
    )

    inconsistente = (
        df["equipo"].astype(str)
        != esperado.astype(str)
    )

    if inconsistente.any():
        return [
            "Existen registros donde "
            "equipo no coincide con la combinación "
            "línea-máquina."
        ]

    return []


def _validar_variables_continuas(
    df: pd.DataFrame,
) -> list[str]:
    """Valida variables continuas numéricas."""
    errores: list[str] = []

    for columna in CONTINUOUS_COLUMNS:
        if not pd.api.types.is_numeric_dtype(
            df[columna]
        ):
            errores.append(
                f"{columna} debe ser numérica."
            )

    return errores


def obtener_errores_validacion(
    df: pd.DataFrame,
) -> list[str]:
    """Devuelve todas las reglas incumplidas."""
    _validar_tipo(df)

    errores = _validar_columnas_obligatorias(df)

    if errores:
        return errores

    errores.extend(_validar_nulos(df))
    errores.extend(_validar_fechas(df))
    errores.extend(_validar_equipo(df))
    errores.extend(_validar_produccion(df))
    errores.extend(_validar_perdidas(df))
    errores.extend(_validar_variables_continuas(df))

    return errores


def validar_dataset(
    df: pd.DataFrame,
) -> None:
    """Valida estructural y operacionalmente el dataset."""
    errores = obtener_errores_validacion(df)

    if errores:
        raise ValueError(" | ".join(errores))


def obtener_reporte_validacion(
    df: pd.DataFrame,
) -> dict[str, Any]:
    """Genera un reporte estructurado de calidad."""
    _validar_tipo(df)

    errores = obtener_errores_validacion(df)

    total_celdas = int(
        df.shape[0] * df.shape[1]
    )

    celdas_nulas = int(
        df.isna().sum().sum()
    )

    completitud = (
        1 - (celdas_nulas / total_celdas)
        if total_celdas > 0
        else 0.0
    )

    return {
        "valido": len(errores) == 0,
        "estado": (
            "Válido"
            if not errores
            else "Con observaciones"
        ),
        "filas": int(df.shape[0]),
        "columnas": int(df.shape[1]),
        "celdas_nulas": celdas_nulas,
        "completitud": round(
            completitud,
            4,
        ),
        "errores": errores,
        "numero_errores": len(errores),
    }
