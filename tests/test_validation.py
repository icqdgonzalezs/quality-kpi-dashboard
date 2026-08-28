"""Tests for dataset validation."""

import pandas as pd
import pytest

from src.validation import (
    obtener_errores_validacion,
    obtener_reporte_validacion,
    validar_dataset,
)


@pytest.fixture
def dataset_valido() -> pd.DataFrame:
    """Dataset mínimo válido para las pruebas."""
    return pd.DataFrame(
        {
            "lote": ["L0001", "L0002"],
            "fecha": ["2025-01-01", "2025-01-02"],
            "linea": ["Línea 1", "Línea 2"],
            "maquina": ["M01", "M04"],
            "equipo": ["L1-M01", "L2-M04"],
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


# ---------------------------------------------------------------------
# VALIDACIÓN GENERAL
# ---------------------------------------------------------------------


def test_dataset_valido_no_lanza_error(dataset_valido):
    """Un dataset válido no debe generar excepciones."""
    validar_dataset(dataset_valido)


def test_falla_si_entrada_no_es_dataframe():
    """La entrada debe ser un pandas.DataFrame."""
    with pytest.raises(
        TypeError,
        match="pandas.DataFrame",
    ):
        validar_dataset([1, 2, 3])


# ---------------------------------------------------------------------
# ESTRUCTURA
# ---------------------------------------------------------------------


def test_falla_si_falta_una_columna(dataset_valido):
    """Debe detectar columnas obligatorias ausentes."""
    df = dataset_valido.drop(columns=["maquina"])

    with pytest.raises(
        ValueError,
        match="Faltan columnas obligatorias",
    ):
        validar_dataset(df)


def test_falla_si_falta_equipo(dataset_valido):
    """Equipo debe ser una columna obligatoria."""
    df = dataset_valido.drop(columns=["equipo"])

    with pytest.raises(
        ValueError,
        match="Faltan columnas obligatorias",
    ):
        validar_dataset(df)


# ---------------------------------------------------------------------
# CALIDAD DE DATOS
# ---------------------------------------------------------------------


def test_falla_si_hay_nulos(dataset_valido):
    """Los campos obligatorios no deben contener nulos."""
    df = dataset_valido.copy()
    df.loc[0, "unidades_producidas"] = None

    with pytest.raises(
        ValueError,
        match="valores nulos",
    ):
        validar_dataset(df)


def test_falla_si_hay_fecha_invalida(dataset_valido):
    """Debe detectar fechas imposibles o con formato inválido."""
    df = dataset_valido.copy()
    df.loc[0, "fecha"] = "fecha_invalida"

    with pytest.raises(
        ValueError,
        match="fechas inválidas",
    ):
        validar_dataset(df)


# ---------------------------------------------------------------------
# IDENTIDAD DEL EQUIPO
# ---------------------------------------------------------------------


def test_equipo_corresponde_a_linea_y_maquina(dataset_valido):
    """La identidad del equipo debe ser consistente con línea y máquina."""
    errores = obtener_errores_validacion(dataset_valido)

    assert not any(
        "equipo no coincide" in error
        for error in errores
    )


def test_falla_si_equipo_no_corresponde_a_linea_y_maquina(
    dataset_valido,
):
    """Debe detectar equipos mal asociados a su línea."""
    df = dataset_valido.copy()

    df.loc[0, "equipo"] = "L2-M01"

    with pytest.raises(
        ValueError,
        match="equipo no coincide",
    ):
        validar_dataset(df)


def test_falla_si_equipo_tiene_formato_inconsistente(
    dataset_valido,
):
    """Debe rechazar un identificador de equipo incorrecto."""
    df = dataset_valido.copy()

    df.loc[0, "equipo"] = "M01"

    with pytest.raises(
        ValueError,
        match="equipo no coincide",
    ):
        validar_dataset(df)


# ---------------------------------------------------------------------
# PRODUCCIÓN
# ---------------------------------------------------------------------


def test_falla_si_hay_unidades_producidas_no_positivas(
    dataset_valido,
):
    """La producción debe ser estrictamente positiva."""
    df = dataset_valido.copy()
    df.loc[0, "unidades_producidas"] = 0

    with pytest.raises(
        ValueError,
        match="unidades_producidas",
    ):
        validar_dataset(df)


def test_falla_si_hay_produccion_negativa(dataset_valido):
    """La producción negativa debe ser rechazada."""
    df = dataset_valido.copy()
    df.loc[0, "unidades_producidas"] = -100

    with pytest.raises(
        ValueError,
        match="unidades_producidas",
    ):
        validar_dataset(df)


def test_falla_si_defectuosas_superan_producidas(
    dataset_valido,
):
    """Los defectuosos no pueden superar la producción."""
    df = dataset_valido.copy()
    df.loc[0, "unidades_defectuosas"] = 1100

    with pytest.raises(
        ValueError,
        match="defectuosas",
    ):
        validar_dataset(df)


# ---------------------------------------------------------------------
# SCRAP / REPROCESO
# ---------------------------------------------------------------------


def test_falla_si_scrap_es_negativo(dataset_valido):
    """Scrap debe ser no negativo."""
    df = dataset_valido.copy()
    df.loc[0, "unidades_scrap"] = -1

    with pytest.raises(
        ValueError,
        match="unidades_scrap",
    ):
        validar_dataset(df)


def test_falla_si_reproceso_es_negativo(dataset_valido):
    """Reproceso debe ser no negativo."""
    df = dataset_valido.copy()
    df.loc[0, "unidades_reproceso"] = -1

    with pytest.raises(
        ValueError,
        match="unidades_reproceso",
    ):
        validar_dataset(df)


def test_falla_si_scrap_y_reproceso_no_reconcilian(
    dataset_valido,
):
    """Scrap + reproceso debe coincidir con defectuosas."""
    df = dataset_valido.copy()
    df.loc[0, "unidades_scrap"] = 20

    with pytest.raises(
        ValueError,
        match="scrap.*reproceso",
    ):
        validar_dataset(df)


# ---------------------------------------------------------------------
# VARIABLES CONTINUAS
# ---------------------------------------------------------------------


def test_falla_si_peso_no_es_numerico(dataset_valido):
    """Peso promedio debe ser numérico."""
    df = dataset_valido.copy()
    df["peso_promedio"] = [
        "quinientos",
        499.8,
    ]

    with pytest.raises(
        ValueError,
        match="peso_promedio debe ser numérica",
    ):
        validar_dataset(df)


def test_falla_si_longitud_no_es_numerica(
    dataset_valido,
):
    """Longitud promedio debe ser numérica."""
    df = dataset_valido.copy()
    df["longitud_promedio"] = [
        "ciento veinte",
        120.2,
    ]

    with pytest.raises(
        ValueError,
        match="longitud_promedio debe ser numérica",
    ):
        validar_dataset(df)


# ---------------------------------------------------------------------
# REPORTE DE VALIDACIÓN
# ---------------------------------------------------------------------


def test_obtener_errores_validacion_dataset_valido(
    dataset_valido,
):
    """Un dataset válido debe devolver cero errores."""
    errores = obtener_errores_validacion(
        dataset_valido
    )

    assert errores == []


def test_obtener_errores_validacion_detecta_multiple_errores(
    dataset_valido,
):
    """La API debe acumular múltiples errores."""
    df = dataset_valido.copy()

    df.loc[0, "fecha"] = "fecha_invalida"
    df.loc[0, "unidades_producidas"] = 0
    df.loc[0, "unidades_scrap"] = -1

    errores = obtener_errores_validacion(df)

    assert len(errores) >= 3


def test_reporte_validacion_dataset_valido(
    dataset_valido,
):
    """El reporte debe describir correctamente un dataset válido."""
    reporte = obtener_reporte_validacion(
        dataset_valido
    )

    assert reporte["valido"] is True
    assert reporte["estado"] == "Válido"
    assert reporte["filas"] == 2
    assert reporte["columnas"] == 14
    assert reporte["celdas_nulas"] == 0
    assert reporte["completitud"] == 1.0
    assert reporte["numero_errores"] == 0
    assert reporte["errores"] == []


def test_reporte_validacion_dataset_con_nulos(
    dataset_valido,
):
    """El reporte debe identificar pérdida de completitud."""
    df = dataset_valido.copy()
    df.loc[0, "peso_promedio"] = None

    reporte = obtener_reporte_validacion(df)

    assert reporte["valido"] is False
    assert reporte["estado"] == "Con observaciones"
    assert reporte["celdas_nulas"] == 1
    assert reporte["completitud"] < 1.0
    assert reporte["numero_errores"] >= 1


def test_reporte_validacion_dataset_no_dataframe():
    """El reporte también debe validar el tipo de entrada."""
    with pytest.raises(
        TypeError,
        match="pandas.DataFrame",
    ):
        obtener_reporte_validacion([1, 2, 3])