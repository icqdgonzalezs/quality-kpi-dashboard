"""Vista general de la planta y estado analítico de equipos."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.kpis import calcular_kpis_por_dimension

from dashboard.components.theme import (
    get_status_color,
    get_status_symbol,
)


def _estado_equipo(
    tasa: float,
    promedio: float,
    desviacion: float,
) -> str:
    """Clasifica el desempeño relativo del equipo."""
    if desviacion == 0:
        return (
            "NORMAL"
            if tasa <= promedio
            else "WATCH"
        )

    limite_watch = promedio + (
        0.5 * desviacion
    )

    limite_priority = promedio + desviacion

    if tasa <= limite_watch:
        return "NORMAL"

    if tasa <= limite_priority:
        return "WATCH"

    return "PRIORITY"


def renderizar_plant_overview(
    df: pd.DataFrame,
) -> None:
    """Renderiza el estado analítico de los 8 equipos."""

    st.markdown(
        '<div class="section-label">PLANT OVERVIEW</div>',
        unsafe_allow_html=True,
    )

    st.subheader("Estado operacional de equipos")

    st.caption(
        "Estado relativo al desempeño observado en el universo seleccionado."
    )

    ranking = calcular_kpis_por_dimension(
        df,
        "equipo",
    )

    if ranking.empty:
        st.info(
            "No existen equipos disponibles."
        )
        return

    promedio = ranking[
        "tasa_defectos"
    ].mean()

    desviacion = ranking[
        "tasa_defectos"
    ].std(ddof=0)

    for linea, prefijo in [
        ("Línea 1", "L1"),
        ("Línea 2", "L2"),
    ]:

        equipos_linea = ranking[
            ranking["equipo"].str.startswith(
                f"{prefijo}-"
            )
        ]

        if equipos_linea.empty:
            continue

        st.markdown(
            f"**{linea}**"
        )

        columnas = st.columns(4)

        for indice in range(1, 5):

            equipo_id = (
                f"{prefijo}-M0{indice}"
            )

            with columnas[indice - 1]:

                fila = equipos_linea[
                    equipos_linea["equipo"]
                    == equipo_id
                ]

                if fila.empty:

                    st.metric(
                        equipo_id,
                        "N/D",
                    )

                    continue

                fila = fila.iloc[0]

                tasa = float(
                    fila["tasa_defectos"]
                )

                estado = _estado_equipo(
                    tasa,
                    float(promedio),
                    float(desviacion),
                )

                color = get_status_color(
                    estado
                )

                simbolo = get_status_symbol(
                    estado
                )

                st.metric(
                    equipo_id,
                    f"{tasa:.2%}",
                    f"{simbolo} {estado}",
                )

                st.markdown(
                    f"""
                    <div style="
                        height: 4px;
                        width: 100%;
                        border-radius: 4px;
                        background: {color};
                        margin-top: -8px;
                        margin-bottom: 8px;
                    "></div>
                    """,
                    unsafe_allow_html=True,
                )

                st.caption(
                    f"{int(fila['n_lotes'])} lotes · "
                    f"{int(fila['unidades_defectuosas']):,} "
                    "defectuosas"
                )

        st.divider()
