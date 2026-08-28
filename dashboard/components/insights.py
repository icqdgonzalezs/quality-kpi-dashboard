"""Hallazgos accionables derivados del universo analizado."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.kpis import calcular_kpis_por_dimension


def renderizar_insights(
    df: pd.DataFrame,
    cpk_min: float | None,
    variable_cpk: str,
) -> None:
    """Renderiza las prioridades analíticas."""

    st.markdown(
        '<div class="section-label">ACTIONABLE INSIGHTS</div>',
        unsafe_allow_html=True,
    )

    st.subheader("Prioridades para investigación")

    st.caption(
        "Los hallazgos priorizan análisis; no sustituyen el análisis de causa raíz."
    )

    equipos = calcular_kpis_por_dimension(
        df,
        "equipo",
    )

    turnos = calcular_kpis_por_dimension(
        df,
        "turno",
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown("### 🛠️ Equipo prioritario")

        if equipos.empty:

            st.info("Sin datos.")

        else:

            fila = equipos.iloc[0]

            st.metric(
                "Equipo",
                fila["equipo"],
                f"{fila['tasa_defectos']:.2%}",
            )

            st.caption(
                f"{int(fila['n_lotes'])} lotes · "
                f"{int(fila['unidades_defectuosas']):,} "
                "unidades defectuosas"
            )

            st.caption(
                "Investigar condiciones operacionales, "
                "mantenimiento y causas asignables."
            )

    with c2:

        st.markdown("### 🌙 Turno prioritario")

        if turnos.empty:

            st.info("Sin datos.")

        else:

            fila = turnos.iloc[0]

            st.metric(
                "Turno",
                fila["turno"],
                f"{fila['tasa_defectos']:.2%}",
            )

            st.caption(
                f"{int(fila['n_lotes'])} lotes"
            )

            st.caption(
                "Revisar carga operacional, "
                "supervisión y estabilidad."
            )

    with c3:

        st.markdown("### 📐 Capacidad crítica")

        if cpk_min is None:

            st.info("Sin datos.")

        else:

            st.metric(
                "Variable",
                variable_cpk,
                f"Cpk {cpk_min:.2f}",
            )

            if cpk_min >= 1.33:

                st.caption(
                    "CAPABLE · Mantener monitoreo."
                )

            elif cpk_min >= 1.00:

                st.caption(
                    "MARGINAL · Reducir variabilidad."
                )

            else:

                st.caption(
                    "NOT CAPABLE · Priorizar acción correctiva."
                )
