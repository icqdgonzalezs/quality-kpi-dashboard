import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
import pytest
from src.kpis import calcular_kpis_globales, calcular_kpis_por_dimension, calcular_pareto, identificar_lote_critico

@pytest.fixture
def df_muestra():
    return pd.DataFrame({
        "lote": ["L1", "L2", "L3"],
        "unidades_producidas": [100, 200, 100],
        "unidades_defectuosas": [10, 10, 30],
        "unidades_scrap": [3, 3, 9],
        "unidades_reproceso": [7, 7, 21],
        "defecto_tipo": ["Mancha", "Rayadura", "Mancha"],
        "maquina": ["M01", "M02", "M01"],
    })

def test_kpis_globales_fpy(df_muestra):
    kpis = calcular_kpis_globales(df_muestra)
    assert kpis["fpy"] == pytest.approx((400-50)/400)
    assert kpis["total_defectuosas"] == 50

def test_kpis_por_dimension(df_muestra):
    r = calcular_kpis_por_dimension(df_muestra, "maquina")
    assert set(r["maquina"]) == {"M01", "M02"}
    m01 = r[r["maquina"]=="M01"].iloc[0]
    assert m01["tasa_defectos"] == pytest.approx(40/200)

def test_kpis_por_dimension_invalida(df_muestra):
    with pytest.raises(ValueError):
        calcular_kpis_por_dimension(df_muestra, "columna_inexistente")

def test_pareto(df_muestra):
    p = calcular_pareto(df_muestra)
    assert p.iloc[0]["defecto"] == "Mancha"
    assert p["porcentaje_acumulado"].iloc[-1] == pytest.approx(100.0)

def test_lote_critico_por_tasa_no_conteo(df_muestra):
    # L3 tiene 30/100=30% (mayor tasa), aunque L2 tenga mismo conteo absoluto que L1
    critico = identificar_lote_critico(df_muestra)
    assert critico["lote"] == "L3"
