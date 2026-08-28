"""Control Center: filtros y construcción del universo analítico."""

from __future__ import annotations

import pandas as pd
import streamlit as st


# =====================================================================
# RESTABLECER FILTROS
# =====================================================================

def restablecer_filtros() -> None:
    """
    Solicita una nueva versión de widgets.

    Se utiliza exclusivamente para restaurar las selecciones.
    """
    st.session_state["filtros_reset_version"] = (
        st.session_state.get(
            "filtros_reset_version",
            0,
        )
        + 1
    )


def obtener_version_widgets() -> int:
    """Obtiene la versión actual de los widgets categóricos."""
    return int(
        st.session_state.get(
            "filtros_reset_version",
            0,
        )
    )


# =====================================================================
# UTILIDADES
# =====================================================================

def _limpiar_estado_selectbox(
    key: str,
    opciones: list[str],
) -> None:
    """Elimina valores persistentes que ya no pertenecen al dominio."""

    if key in st.session_state:

        valor = st.session_state[key]

        if valor not in opciones:
            del st.session_state[key]


def _aplicar_filtro(
    df: pd.DataFrame,
    columna: str,
    valor: str,
    valor_todos: str,
) -> pd.DataFrame:
    """Aplica un filtro categórico cuando existe una selección concreta."""

    if valor == valor_todos:
        return df

    return df[
        df[columna].astype(str) == valor
    ].copy()


# =====================================================================
# CONTROL CENTER
# =====================================================================

def aplicar_filtros(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Renderiza el Control Center y devuelve el universo filtrado.

    Los filtros se aplican automáticamente al cambiar cada selección.
    """

    # ===============================================================
    # VALIDACIÓN
    # ===============================================================

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "El objeto de entrada debe ser un pandas.DataFrame."
        )

    if df.empty:
        return df.copy()

    datos = df.copy()

    # ===============================================================
    # PREPARAR FECHAS
    # ===============================================================

    datos["fecha"] = pd.to_datetime(
        datos["fecha"],
        errors="coerce",
    )

    if datos["fecha"].isna().all():
        raise ValueError(
            "La columna 'fecha' no contiene fechas válidas."
        )

    fecha_min = datos["fecha"].min().date()
    fecha_max = datos["fecha"].max().date()

    # ===============================================================
    # VERSION DE WIDGETS CATEGÓRICOS
    # ===============================================================

    version = obtener_version_widgets()

    # ===============================================================
    # CONTROL CENTER
    # ===============================================================

    st.sidebar.markdown(
        "## 🎛️ Centro de control"
    )

    st.sidebar.caption(
        "Define el universo operativo que quieres analizar."
    )

    # ===============================================================
    # RESTAURAR FILTROS
    # ===============================================================

    st.sidebar.button(
        "↩️ Restaurar filtros",
        width='stretch',
        on_click=restablecer_filtros,
    )

    # ===============================================================
    # PERÍODO
    # ===============================================================
    #
    # IMPORTANTE:
    # No se manipula manualmente session_state para este widget.
    # Se utiliza una clave nueva y fija para abandonar cualquier estado
    # antiguo como periodo_filtro_0 / periodo_filtro_v2_0.
    #
    # Streamlit administra automáticamente el valor seleccionado.
    # ===============================================================

    periodo = st.sidebar.date_input(
        "Período",
        value=(
            fecha_min,
            fecha_max,
        ),
        min_value=fecha_min,
        max_value=fecha_max,
        key="periodo_filtro_final",
    )

    if isinstance(periodo, tuple) and len(periodo) == 2:

        fecha_inicio = periodo[0]
        fecha_fin = periodo[1]

    elif isinstance(periodo, list) and len(periodo) == 2:

        fecha_inicio = periodo[0]
        fecha_fin = periodo[1]

    else:

        fecha_inicio = periodo
        fecha_fin = periodo

    # ===============================================================
    # FILTRO TEMPORAL
    # ===============================================================

    df_filtrado = datos[
        (datos["fecha"].dt.date >= fecha_inicio)
        & (datos["fecha"].dt.date <= fecha_fin)
    ].copy()

    # ===============================================================
    # LÍNEA
    # ===============================================================

    lineas = [
        "Todas",
        *sorted(
            df_filtrado["linea"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        ),
    ]

    linea_key = (
        "linea_filtro_final_"
        + str(version)
    )

    _limpiar_estado_selectbox(
        linea_key,
        lineas,
    )

    linea = st.sidebar.selectbox(
        "Línea",
        lineas,
        index=0,
        key=linea_key,
    )

    df_filtrado = _aplicar_filtro(
        df_filtrado,
        "linea",
        linea,
        "Todas",
    )

    # ===============================================================
    # EQUIPO
    # ===============================================================

    equipos = sorted(
        df_filtrado["equipo"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    opciones_equipo = [
        "Todos",
        *equipos,
    ]

    equipo_key = (
        "equipo_filtro_final_"
        + str(version)
    )

    _limpiar_estado_selectbox(
        equipo_key,
        opciones_equipo,
    )

    equipo = st.sidebar.selectbox(
        "Equipo",
        opciones_equipo,
        index=0,
        key=equipo_key,
    )

    df_filtrado = _aplicar_filtro(
        df_filtrado,
        "equipo",
        equipo,
        "Todos",
    )

    # ===============================================================
    # TURNO
    # ===============================================================

    turnos = sorted(
        df_filtrado["turno"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    opciones_turno = [
        "Todos",
        *turnos,
    ]

    turno_key = (
        "turno_filtro_final_"
        + str(version)
    )

    _limpiar_estado_selectbox(
        turno_key,
        opciones_turno,
    )

    turno = st.sidebar.selectbox(
        "Turno",
        opciones_turno,
        index=0,
        key=turno_key,
    )

    df_filtrado = _aplicar_filtro(
        df_filtrado,
        "turno",
        turno,
        "Todos",
    )

    # ===============================================================
    # OPERADOR
    # ===============================================================

    operadores = sorted(
        df_filtrado["operador"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    opciones_operador = [
        "Todos",
        *operadores,
    ]

    operador_key = (
        "operador_filtro_final_"
        + str(version)
    )

    _limpiar_estado_selectbox(
        operador_key,
        opciones_operador,
    )

    operador = st.sidebar.selectbox(
        "Operador",
        opciones_operador,
        index=0,
        key=operador_key,
    )

    df_filtrado = _aplicar_filtro(
        df_filtrado,
        "operador",
        operador,
        "Todos",
    )

    # ===============================================================
    # DEVOLVER UNIVERSO
    # ===============================================================

    return df_filtrado
