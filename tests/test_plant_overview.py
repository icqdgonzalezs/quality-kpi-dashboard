import pandas as pd

from dashboard.plant_overview import (
    calcular_estado_equipo,
    construir_ranking_equipos,
)


def test_construir_ranking_equipos_devuelve_metricas_por_equipo():
    df = pd.DataFrame(
        {
            "equipo": ["L1-M01", "L1-M01", "L1-M02"],
            "unidades_producidas": [100, 100, 100],
            "unidades_defectuosas": [10, 10, 5],
            "unidades_scrap": [3, 3, 2],
            "unidades_reproceso": [7, 7, 3],
            "lote": ["L1", "L2", "L3"],
        }
    )

    ranking = construir_ranking_equipos(df)

    assert list(ranking["equipo"]) == ["L1-M01", "L1-M02"]
    assert "tasa_defectos" in ranking.columns
    assert "n_lotes" in ranking.columns


def test_estado_normal():
    assert calcular_estado_equipo(
        tasa=0.02,
        promedio=0.03,
        desviacion=0.01,
    ) == "NORMAL"


def test_estado_watch():
    assert calcular_estado_equipo(
        tasa=0.035,
        promedio=0.03,
        desviacion=0.01,
    ) == "WATCH"


def test_estado_priority():
    assert calcular_estado_equipo(
        tasa=0.045,
        promedio=0.03,
        desviacion=0.01,
    ) == "PRIORITY"


def test_estado_con_desviacion_cero():
    assert calcular_estado_equipo(
        tasa=0.03,
        promedio=0.03,
        desviacion=0.0,
    ) == "NORMAL"

    assert calcular_estado_equipo(
        tasa=0.04,
        promedio=0.03,
        desviacion=0.0,
    ) == "WATCH"


def test_ranking_vacio():
    ranking = construir_ranking_equipos(pd.DataFrame())

    assert ranking.empty
