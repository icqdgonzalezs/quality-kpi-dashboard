import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
import pytest
from src.capability import calcular_cp_cpk, resumen_capacidad

def test_cp_cpk_valores_conocidos():
    valores = pd.Series([98,99,100,101,102,100,99,101,100,100])
    r = calcular_cp_cpk(valores, lsl=90, usl=110)
    assert r["cp"] is not None
    assert r["clasificacion"] in ["Capaz (excelente)", "Marginal (monitorear)", "No capaz (acción requerida)"]

def test_cp_cpk_datos_insuficientes():
    r = calcular_cp_cpk(pd.Series([100]), lsl=90, usl=110)
    assert r["cp"] is None
    assert r["clasificacion"] == "Datos insuficientes"

def test_cp_cpk_limites_invalidos():
    r = calcular_cp_cpk(pd.Series([1,2,3]), lsl=110, usl=90)
    assert r["cp"] is None

def test_cp_cpk_sin_variabilidad():
    r = calcular_cp_cpk(pd.Series([100,100,100]), lsl=90, usl=110)
    assert r["cp"] == float("inf")

def test_cp_cpk_descentrado_penaliza():
    # proceso descentrado hacia USL: Cpk debe ser menor que Cp
    valores = pd.Series([104,105,106,105,104,105,106,105])
    r = calcular_cp_cpk(valores, lsl=90, usl=110)
    assert r["cpk"] < r["cp"]

def test_resumen_capacidad(tmp_path):
    df = pd.DataFrame({"peso": [98,100,102,99,101]*10})
    config = {"peso": {"nombre": "Peso", "lsl": 90, "usl": 110}}
    r = resumen_capacidad(df, config)
    assert len(r) == 1
    assert r.iloc[0]["variable"] == "Peso"
