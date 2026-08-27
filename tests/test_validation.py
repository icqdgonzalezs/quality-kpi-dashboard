"""Tests for dataset validation."""

import pandas as pd
import pytest

from src.validation import validar_dataset


@pytest.fixture
def dataset_valido() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "lote": ["L0001", "L0002"],
            "fecha": ["2025-01-01", "2025-01-02"],
            "linea": ["Línea 1", "Línea 2"],
            "maquina": ["M01", "M04"],
            "turno": ["Mañana", "Noche"],
            "operador": ["Operador A", "Operador B"],
            "unidades_producidas": [1000, 950],
            "unidades_defectuosas": [40, 50],
            "unidades_reproceso": [28, 35],
            "unidades_scrap": [12, 15],
            "defecto_tipo": ["Mancha", "Rayadura"],
            "peso_promedio": [500.1, 499.8],
            "longitud_promedio": [120.0, 120.2],
        }
    )


def test_dataset_valido_no_lanza_error(dataset_valido):
    validar_dataset(dataset_valido)


def test_falla_si_falta_una_columna(dataset_valido):
    df = dataset_valido.drop(columns=["maquina"])

    with pytest.raises(ValueError, match="Faltan columnas obligatorias"):
        validar_dataset(df)


def test_falla_si_hay_nulos(dataset_valido):
    df = dataset_valido.copy()
    df.loc[0, "unidades_producidas"] = None

    with pytest.raises(ValueError, match="valores nulos"):
        validar_dataset(df)


def test_falla_si_hay_fecha_invalida(dataset_valido):
    df = dataset_valido.copy()
    df.loc[0, "fecha"] = "fecha_invalida"

    with pytest.raises(ValueError, match="fechas inválidas"):
        validar_dataset(df)


def test_falla_si_hay_unidades_producidas_no_positivas(dataset_valido):
    df = dataset_valido.copy()
    df.loc[0, "unidades_producidas"] = 0

    with pytest.raises(ValueError, match="unidades_producidas"):
        validar_dataset(df)


def test_falla_si_defectuosas_superan_producidas(dataset_valido):
    df = dataset_valido.copy()
    df.loc[0, "unidades_defectuosas"] = 1100

    with pytest.raises(ValueError, match="defectuosas"):
        validar_dataset(df)


def test_falla_si_scrap_es_negativo(dataset_valido):
    df = dataset_valido.copy()
    df.loc[0, "unidades_scrap"] = -1

    with pytest.raises(ValueError, match="unidades_scrap"):
        validar_dataset(df)


def test_falla_si_reproceso_es_negativo(dataset_valido):
    df = dataset_valido.copy()
    df.loc[0, "unidades_reproceso"] = -1

    with pytest.raises(ValueError, match="unidades_reproceso"):
        validar_dataset(df)


def test_falla_si_scrap_y_reproceso_no_reconcilian(dataset_valido):
    df = dataset_valido.copy()
    df.loc[0, "unidades_scrap"] = 20

    with pytest.raises(ValueError, match="scrap.*reproceso"):
        validar_dataset(df)


def test_falla_si_peso_no_es_numerico(dataset_valido):
    df = dataset_valido.copy()
    df["peso_promedio"] = ["quinientos", 499.8]

    with pytest.raises(ValueError, match="peso_promedio debe ser numérica"):
        validar_dataset(df)


def test_falla_si_longitud_no_es_numerica(dataset_valido):
    df = dataset_valido.copy()
    df["longitud_promedio"] = ["ciento veinte", 120.2]

    with pytest.raises(
        ValueError,
        match="longitud_promedio debe ser numérica",
    ):
        validar_dataset(df)


def test_falla_si_entrada_no_es_dataframe():
    with pytest.raises(
        TypeError,
        match="pandas.DataFrame",
    ):
        validar_dataset([1, 2, 3])
