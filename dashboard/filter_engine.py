from __future__ import annotations

import pandas as pd


FILTER_COLUMNS = (
    "linea",
    "equipo",
    "turno",
    "operador",
)


def aplicar_filtro(
    df: pd.DataFrame,
    columna: str,
    valor: str,
    valor_todos: str = "Todos",
) -> pd.DataFrame:
    """Aplica un filtro categórico sin depender de ningún framework de UI."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("El objeto de entrada debe ser un pandas.DataFrame.")

    if columna not in df.columns:
        raise ValueError(f"La columna '{columna}' no existe en el dataset.")

    if valor == valor_todos:
        return df.copy()

    return df[df[columna].astype(str) == str(valor)].copy()


def aplicar_filtros(
    df: pd.DataFrame,
    fecha_inicio=None,
    fecha_fin=None,
    linea: str = "Todas",
    equipo: str = "Todos",
    turno: str = "Todos",
    operador: str = "Todos",
) -> pd.DataFrame:
    """
    Aplica el universo analítico de forma determinista.

    Orden:
    período → línea → equipo → turno → operador.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("El objeto de entrada debe ser un pandas.DataFrame.")

    if df.empty:
        return df.copy()

    datos = df.copy()

    if "fecha" not in datos.columns:
        raise ValueError("La columna 'fecha' no existe en el dataset.")

    datos["fecha"] = pd.to_datetime(
        datos["fecha"],
        errors="coerce",
        format="mixed",
    )

    if datos["fecha"].isna().all():
        raise ValueError("La columna 'fecha' no contiene fechas válidas.")

    if fecha_inicio is not None:
        fecha_inicio = pd.to_datetime(fecha_inicio).date()
        datos = datos[datos["fecha"].dt.date >= fecha_inicio].copy()

    if fecha_fin is not None:
        fecha_fin = pd.to_datetime(fecha_fin).date()
        datos = datos[datos["fecha"].dt.date <= fecha_fin].copy()

    valores = {
        "linea": (linea, "Todas"),
        "equipo": (equipo, "Todos"),
        "turno": (turno, "Todos"),
        "operador": (operador, "Todos"),
    }

    for columna, (valor, valor_todos) in valores.items():
        datos = aplicar_filtro(
            datos,
            columna,
            valor,
            valor_todos,
        )

    return datos.reset_index(drop=True)
