"""Tarjetas KPI del dashboard."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.components.theme import COLORS


def _estado_cpk(
    cpk: float | None,
) -> tuple[str, str]:
    """Clasifica el Cpk para presentación."""
    if cpk is None:
        return "NO DATA", COLORS["reference"]

    if cpk >= 1.33:
        return "NORMAL", COLORS["normal"]

    if cpk >= 1.00:
        return "WATCH", COLORS["warning"]

    return "PRIORITY", COLORS["critical"]


def renderizar_kpis(
    kpis: dict,
    cpk_min: float | None,
    variable_cpk: str,
    lote_critico: pd.Series,
) -> None:
    """Renderiza el resumen ejecutivo."""

    st.markdown(
        '<div class="section-label">EXECUTIVE OVERVIEW</div>',
        unsafe_allow_html=True,
    )

    st.subheader(
        "Situación operacional"
    )

    columnas = st.columns(5)

    with columnas[0]:

        st.metric(
            "FPY",
            f"{kpis['fpy']:.1%}",
        )

        st.caption(
            "First Pass Yield"
        )

    with columnas[1]:

        st.metric(
            "Tasa de defectos",
            f"{kpis['tasa_defectos']:.2%}",
        )

        st.caption(
            "Defectos / producción"
        )

    with columnas[2]:

        st.metric(
            "Tasa de scrap",
            f"{kpis['tasa_scrap']:.2%}",
        )

        st.caption(
            "Pérdida irrecuperable"
        )

    with columnas[3]:

        if cpk_min is None:

            st.metric(
                "Cpk crítico",
                "N/D",
            )

            st.caption(
                "Sin datos"
            )

        else:

            estado, color = _estado_cpk(
                cpk_min
            )

            st.metric(
                "Cpk crítico",
                f"{cpk_min:.2f}",
                variable_cpk,
            )

            st.markdown(
                f"""
                <div style="
                    color: {color};
                    font-size: 0.78rem;
                    font-weight: 700;
                    margin-top: -8px;
                ">
                    ● {estado}
                </div>
                """,
                unsafe_allow_html=True,
            )

    with columnas[4]:

        st.metric(
            "Lote crítico",
            str(
                lote_critico["lote"]
            ),
            f"{lote_critico['tasa_defectos_lote']:.2%}",
        )

        st.caption(
            "Mayor tasa de defectos"
        )
