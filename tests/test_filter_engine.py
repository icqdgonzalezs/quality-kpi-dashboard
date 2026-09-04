import pandas as pd
import pytest

from dashboard.filter_engine import aplicar_filtro, aplicar_filtros


@pytest.fixture
def df_filtros():
    return pd.DataFrame(
        {
            "fecha": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-02",
                    "2024-01-03",
                    "2024-01-04",
                ]
            ),
            "linea": ["Línea 1", "Línea 1", "Línea 2", "Línea 2"],
            "equipo": ["M01", "M02", "M01", "M02"],
            "turno": ["Mañana", "Noche", "Mañana", "Noche"],
            "operador": ["OP01", "OP02", "OP01", "OP02"],
        }
    )


def test_aplicar_filtro_returns_matching_rows(df_filtros):
    resultado = aplicar_filtro(
        df_filtros,
        "linea",
        "Línea 1",
    )

    assert len(resultado) == 2
    assert resultado["linea"].eq("Línea 1").all()


def test_aplicar_filtro_all_returns_copy(df_filtros):
    resultado = aplicar_filtro(
        df_filtros,
        "linea",
        "Todos",
    )

    assert len(resultado) == len(df_filtros)
    assert resultado is not df_filtros


def test_aplicar_filtro_rejects_missing_column(df_filtros):
    with pytest.raises(ValueError, match="no existe"):
        aplicar_filtro(
            df_filtros,
            "producto",
            "PRD-A",
        )


def test_aplicar_filtro_rejects_non_dataframe():
    with pytest.raises(TypeError, match="DataFrame"):
        aplicar_filtro(
            [],
            "linea",
            "Línea 1",
        )


def test_aplicar_filtros_applies_date_range(df_filtros):
    resultado = aplicar_filtros(
        df_filtros,
        fecha_inicio="2024-01-02",
        fecha_fin="2024-01-03",
    )

    assert len(resultado) == 2


def test_aplicar_filtros_applies_all_dimensions(df_filtros):
    resultado = aplicar_filtros(
        df_filtros,
        fecha_inicio="2024-01-02",
        fecha_fin="2024-01-04",
        linea="Línea 2",
        equipo="M02",
        turno="Noche",
        operador="OP02",
    )

    assert len(resultado) == 1
    assert resultado.iloc[0]["linea"] == "Línea 2"
    assert resultado.iloc[0]["equipo"] == "M02"
    assert resultado.iloc[0]["turno"] == "Noche"
    assert resultado.iloc[0]["operador"] == "OP02"


def test_aplicar_filtros_returns_empty_when_no_match(df_filtros):
    resultado = aplicar_filtros(
        df_filtros,
        linea="Línea inexistente",
    )

    assert resultado.empty


def test_aplicar_filtros_rejects_missing_date_column():
    df = pd.DataFrame(
        {
            "linea": ["Línea 1"],
            "equipo": ["M01"],
            "turno": ["Mañana"],
            "operador": ["OP01"],
        }
    )

    with pytest.raises(ValueError, match="fecha"):
        aplicar_filtros(df)


def test_aplicar_filtros_rejects_non_dataframe():
    with pytest.raises(TypeError, match="DataFrame"):
        aplicar_filtros([])


def test_aplicar_filtros_returns_copy_for_empty_dataframe():
    df = pd.DataFrame(
        columns=["fecha", "linea", "equipo", "turno", "operador"]
    )

    resultado = aplicar_filtros(df)

    assert resultado.empty
    assert resultado is not df


def test_aplicar_filtros_rejects_all_invalid_dates():
    df = pd.DataFrame(
        {
            "fecha": ["fecha-invalida", "otra-fecha-invalida"],
            "linea": ["Línea 1", "Línea 2"],
            "equipo": ["M01", "M02"],
            "turno": ["Mañana", "Noche"],
            "operador": ["OP01", "OP02"],
        }
    )

    with pytest.raises(ValueError, match="fechas válidas"):
        aplicar_filtros(df)
