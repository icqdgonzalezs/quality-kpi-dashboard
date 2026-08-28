"""Tests for industrial quality KPI calculations."""

import pandas as pd
import pytest

from src.kpis import (
    calcular_kpis_globales,
    calcular_kpis_por_dimension,
    calcular_pareto,
    identificar_lote_critico,
)


@pytest.fixture
def df_muestra() -> pd.DataFrame:
    """Dataset mínimo para las pruebas KPI."""
    return pd.DataFrame(
        {
            "lote": ["L1", "L2", "L3"],
            "linea": [
                "Línea 1",
                "Línea 1",
                "Línea 2",
            ],
            "maquina": [
                "M01",
                "M02",
                "M01",
            ],
            "equipo": [
                "L1-M01",
                "L1-M02",
                "L2-M01",
            ],
            "turno": [
                "Mañana",
                "Tarde",
                "Noche",
            ],
            "operador": [
                "Operador A",
                "Operador B",
                "Operador C",
            ],
            "unidades_producidas": [
                100,
                200,
                100,
            ],
            "unidades_defectuosas": [
                10,
                10,
                30,
            ],
            "unidades_scrap": [
                3,
                3,
                9,
            ],
            "unidades_reproceso": [
                7,
                7,
                21,
            ],
            "defecto_tipo": [
                "Mancha",
                "Rayadura",
                "Mancha",
            ],
        }
    )


# ---------------------------------------------------------------------
# KPI GLOBAL
# ---------------------------------------------------------------------


def test_kpis_globales(df_muestra):
    kpis = calcular_kpis_globales(
        df_muestra
    )

    assert kpis["fpy"] == pytest.approx(
        350 / 400
    )

    assert kpis["tasa_defectos"] == pytest.approx(
        50 / 400
    )

    assert kpis["tasa_scrap"] == pytest.approx(
        15 / 400
    )

    assert kpis["tasa_reproceso"] == pytest.approx(
        35 / 400
    )

    assert kpis["total_producidas"] == 400
    assert kpis["total_defectuosas"] == 50
    assert kpis["total_scrap"] == 15
    assert kpis["total_reproceso"] == 35


def test_kpis_globales_usan_totales_y_no_promedio_de_tasas(
    df_muestra,
):
    kpis = calcular_kpis_globales(
        df_muestra
    )

    promedio_tasas = (
        10 / 100
        + 10 / 200
        + 30 / 100
    ) / 3

    assert kpis["tasa_defectos"] != pytest.approx(
        promedio_tasas
    )

    assert kpis["tasa_defectos"] == pytest.approx(
        50 / 400
    )


def test_kpis_fallan_con_dataset_vacio():
    df = pd.DataFrame(
        columns=[
            "lote",
            "unidades_producidas",
            "unidades_defectuosas",
            "unidades_scrap",
            "unidades_reproceso",
        ]
    )

    with pytest.raises(
        ValueError,
        match="vacío",
    ):
        calcular_kpis_globales(df)


def test_kpis_fallan_con_entrada_no_dataframe():
    with pytest.raises(
        TypeError,
        match="pandas.DataFrame",
    ):
        calcular_kpis_globales(
            [1, 2, 3]
        )


def test_kpis_fallan_con_produccion_cero():
    df = pd.DataFrame(
        {
            "lote": ["L1"],
            "unidades_producidas": [0],
            "unidades_defectuosas": [0],
            "unidades_scrap": [0],
            "unidades_reproceso": [0],
        }
    )

    with pytest.raises(
        ValueError,
        match="mayores que cero",
    ):
        calcular_kpis_globales(df)


def test_kpis_fallan_si_defectuosas_superan_produccion(
    df_muestra,
):
    df = df_muestra.copy()

    df.loc[
        0,
        "unidades_defectuosas",
    ] = 101

    with pytest.raises(
        ValueError,
        match="superar",
    ):
        calcular_kpis_globales(df)


def test_kpis_fallan_si_scrap_y_reproceso_no_reconcilian(
    df_muestra,
):
    df = df_muestra.copy()

    df.loc[
        0,
        "unidades_scrap",
    ] = 20

    with pytest.raises(
        ValueError,
        match="Scrap",
    ):
        calcular_kpis_globales(df)


# ---------------------------------------------------------------------
# KPI POR DIMENSIÓN
# ---------------------------------------------------------------------


def test_kpis_por_dimension_maquina(
    df_muestra,
):
    resultado = calcular_kpis_por_dimension(
        df_muestra,
        "maquina",
    )

    assert set(
        resultado["maquina"]
    ) == {
        "M01",
        "M02",
    }

    m01 = resultado[
        resultado["maquina"] == "M01"
    ].iloc[0]

    assert (
        m01["unidades_producidas"]
        == 200
    )

    assert (
        m01["unidades_defectuosas"]
        == 40
    )

    assert m01[
        "tasa_defectos"
    ] == pytest.approx(
        40 / 200
    )

    assert m01["fpy"] == pytest.approx(
        160 / 200
    )


def test_kpis_por_dimension_equipo(
    df_muestra,
):
    resultado = calcular_kpis_por_dimension(
        df_muestra,
        "equipo",
    )

    assert set(
        resultado["equipo"]
    ) == {
        "L1-M01",
        "L1-M02",
        "L2-M01",
    }


def test_kpis_por_dimension_orden_descendente(
    df_muestra,
):
    resultado = calcular_kpis_por_dimension(
        df_muestra,
        "maquina",
    )

    tasas = resultado[
        "tasa_defectos"
    ].tolist()

    assert tasas == sorted(
        tasas,
        reverse=True,
    )


def test_kpis_por_dimension_invalida(
    df_muestra,
):
    with pytest.raises(
        ValueError,
        match="no es válida",
    ):
        calcular_kpis_por_dimension(
            df_muestra,
            "columna_inexistente",
        )


def test_kpis_por_dimension_falta_columna(
    df_muestra,
):
    df = df_muestra.drop(
        columns=["equipo"]
    )

    with pytest.raises(
        ValueError,
        match="no existe",
    ):
        calcular_kpis_por_dimension(
            df,
            "equipo",
        )


# ---------------------------------------------------------------------
# PARETO
# ---------------------------------------------------------------------


def test_pareto_usa_unidades_defectuosas(
    df_muestra,
):
    resultado = calcular_pareto(
        df_muestra
    )

    assert (
        resultado.iloc[0]["defecto"]
        == "Mancha"
    )

    assert (
        resultado.iloc[0]["frecuencia"]
        == 40
    )

    assert (
        resultado[
            "porcentaje_acumulado"
        ].iloc[-1]
        == pytest.approx(100.0)
    )


def test_pareto_sin_defectos_devuelve_dataframe_vacio():
    df = pd.DataFrame(
        {
            "defecto_tipo": [
                "Mancha",
                "Rayadura",
            ],
            "unidades_defectuosas": [
                0,
                0,
            ],
        }
    )

    resultado = calcular_pareto(df)

    assert resultado.empty

    assert list(
        resultado.columns
    ) == [
        "defecto",
        "frecuencia",
        "porcentaje",
        "porcentaje_acumulado",
    ]


def test_pareto_falla_con_defectos_negativos():
    df = pd.DataFrame(
        {
            "defecto_tipo": ["Mancha"],
            "unidades_defectuosas": [-1],
        }
    )

    with pytest.raises(
        ValueError,
        match="no puede ser negativa",
    ):
        calcular_pareto(df)


# ---------------------------------------------------------------------
# LOTE CRÍTICO
# ---------------------------------------------------------------------


def test_lote_critico_por_tasa_no_conteo(
    df_muestra,
):
    critico = identificar_lote_critico(
        df_muestra
    )

    assert critico["lote"] == "L3"

    assert critico[
        "tasa_defectos_lote"
    ] == pytest.approx(0.30)


def test_lote_critico_falla_si_produccion_es_cero(
    df_muestra,
):
    df = df_muestra.copy()

    df.loc[
        0,
        "unidades_producidas",
    ] = 0

    with pytest.raises(
        ValueError,
        match="mayores que cero",
    ):
        identificar_lote_critico(df)


def test_lote_critico_falla_si_defectuosas_superan_produccion(
    df_muestra,
):
    df = df_muestra.copy()

    df.loc[
        0,
        "unidades_defectuosas",
    ] = 150

    with pytest.raises(
        ValueError,
        match="superar",
    ):
        identificar_lote_critico(df)