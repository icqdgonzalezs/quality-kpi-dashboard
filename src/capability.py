"""
Análisis de capacidad de proceso (Cp/Cpk).

Las funciones de este módulo calculan indicadores de capacidad para
variables continuas respecto de límites de especificación definidos
externamente.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def calcular_cp_cpk(
    valores: pd.Series,
    lsl: float,
    usl: float,
) -> dict:
    """Calcula Cp y Cpk para una variable continua.

    Parameters
    ----------
    valores : pd.Series
        Observaciones del proceso.
    lsl : float
        Límite inferior de especificación.
    usl : float
        Límite superior de especificación.

    Returns
    -------
    dict
        Resultados de capacidad y estadísticos descriptivos.

    Notes
    -----
    La interpretación de Cp/Cpk requiere considerar los supuestos
    estadísticos del proceso. Estos índices no demuestran por sí mismos
    que el proceso esté bajo control estadístico.
    """
    if not isinstance(valores, pd.Series):
        valores = pd.Series(valores)

    if not np.isfinite(lsl) or not np.isfinite(usl):
        return {
            "cp": None,
            "cpk": None,
            "media": None,
            "sigma": None,
            "n": 0,
            "clasificacion": "Límites inválidos",
        }

    if usl <= lsl:
        return {
            "cp": None,
            "cpk": None,
            "media": None,
            "sigma": None,
            "n": 0,
            "clasificacion": "Límites inválidos",
        }

    valores = pd.to_numeric(valores, errors="coerce")
    valores = valores.replace([np.inf, -np.inf], np.nan).dropna()

    n = len(valores)

    if n < 2:
        return {
            "cp": None,
            "cpk": None,
            "media": None,
            "sigma": None,
            "n": n,
            "clasificacion": "Datos insuficientes",
        }

    media = float(valores.mean())
    sigma = float(valores.std(ddof=1))

    if sigma == 0:
        if lsl <= media <= usl:
            return {
                "cp": float("inf"),
                "cpk": float("inf"),
                "media": round(media, 3),
                "sigma": 0.0,
                "n": n,
                "clasificacion": "Sin variabilidad",
            }

        return {
            "cp": float("inf"),
            "cpk": float("-inf"),
            "media": round(media, 3),
            "sigma": 0.0,
            "n": n,
            "clasificacion": "No capaz (fuera de especificación)",
        }

    cp = (usl - lsl) / (6 * sigma)

    cpk = min(
        (usl - media) / (3 * sigma),
        (media - lsl) / (3 * sigma),
    )

    if cpk >= 1.33:
        clasificacion = "Capaz (excelente)"
    elif cpk >= 1.00:
        clasificacion = "Marginal (monitorear)"
    else:
        clasificacion = "No capaz (acción requerida)"

    return {
        "cp": round(cp, 3),
        "cpk": round(cpk, 3),
        "media": round(media, 3),
        "sigma": round(sigma, 4),
        "n": n,
        "clasificacion": clasificacion,
    }


def resumen_capacidad(
    df: pd.DataFrame,
    variables_config: dict,
) -> pd.DataFrame:
    """Calcula Cp/Cpk para las variables definidas en configuración."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("El objeto de entrada debe ser un pandas.DataFrame.")

    if df.empty:
        raise ValueError("El dataset no puede estar vacío.")

    filas = []

    for columna, cfg in variables_config.items():
        if columna not in df.columns:
            raise ValueError(
                f"La columna '{columna}' no existe en el dataset."
            )

        for clave in ("nombre", "lsl", "usl"):
            if clave not in cfg:
                raise ValueError(
                    f"La configuración de '{columna}' no contiene '{clave}'."
                )

        resultado = calcular_cp_cpk(
            df[columna],
            lsl=cfg["lsl"],
            usl=cfg["usl"],
        )

        resultado["variable"] = cfg["nombre"]
        resultado["columna"] = columna
        resultado["lsl"] = cfg["lsl"]
        resultado["usl"] = cfg["usl"]

        filas.append(resultado)

    return pd.DataFrame(filas)