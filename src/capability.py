"""
Análisis de capacidad de proceso (Cp/Cpk) según metodología Six Sigma.

Cp: mide la capacidad potencial del proceso (asume centrado perfecto).
    Cp = (USL - LSL) / (6 * sigma)

Cpk: mide la capacidad real, penalizando el descentrado del proceso
     respecto a los límites de especificación.
     Cpk = min[(USL - mu) / (3*sigma), (mu - LSL) / (3*sigma)]

Interpretación estándar de industria:
    Cpk >= 1.33  -> proceso capaz (excelente)
    1.00 <= Cpk < 1.33 -> proceso marginal (aceptable, monitorear)
    Cpk < 1.00   -> proceso NO capaz (requiere acción correctiva)

NOTA METODOLÓGICA: Cp/Cpk asume que los datos siguen una distribución
aproximadamente normal y que el proceso está en control estadístico.
Con n=250 observaciones, la estimación es razonablemente estable
(la literatura recomienda un mínimo de n=30, idealmente n>=100).
"""
import numpy as np
import pandas as pd


def calcular_cp_cpk(valores: pd.Series, lsl: float, usl: float) -> dict:
    """Calcula Cp y Cpk para una serie de valores continuos, dados
    los límites de especificación inferior (lsl) y superior (usl)."""
    valores = valores.dropna()
    n = len(valores)

    if n < 2 or usl <= lsl:
        return {"cp": None, "cpk": None, "media": None, "sigma": None,
                "n": n, "clasificacion": "Datos insuficientes"}

    media = valores.mean()
    sigma = valores.std(ddof=1)

    if sigma == 0:
        return {"cp": float("inf"), "cpk": float("inf"), "media": media,
                "sigma": 0.0, "n": n, "clasificacion": "Sin variabilidad"}

    cp = (usl - lsl) / (6 * sigma)
    cpk = min((usl - media) / (3 * sigma), (media - lsl) / (3 * sigma))

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


def resumen_capacidad(df: pd.DataFrame, variables_config: dict) -> pd.DataFrame:
    """Calcula Cp/Cpk para todas las variables críticas definidas en
    config/quality_config.yaml, retornando una tabla resumen."""
    filas = []
    for col, cfg in variables_config.items():
        resultado = calcular_cp_cpk(df[col], lsl=cfg["lsl"], usl=cfg["usl"])
        resultado["variable"] = cfg["nombre"]
        resultado["columna"] = col
        resultado["lsl"] = cfg["lsl"]
        resultado["usl"] = cfg["usl"]
        filas.append(resultado)
    return pd.DataFrame(filas)
