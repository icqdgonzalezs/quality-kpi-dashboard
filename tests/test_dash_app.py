import pandas as pd
import pytest

from dashboard.dash_app import (
    app,
    actualizar_datos_filtrados,
    actualizar_lineas,
    actualizar_equipos,
    actualizar_turnos,
    actualizar_operadores,
    actualizar_kpis,
)



def test_actualizar_kpis_returns_expected_values():
    data = actualizar_datos_filtrados(
        "2024-01-01",
        "2025-12-31",
        "Todas",
        "Todos",
        "Todos",
        "Todos",
    )

    valores = actualizar_kpis(data)

    assert valores == (
        "249,752",
        "95.4%",
        "4.6%",
        "1.4%",
    )


def test_actualizar_kpis_handles_empty_data():
    assert actualizar_kpis(None) == (
        "0",
        "—",
        "—",
        "—",
    )


def test_actualizar_kpis_rejects_missing_columns():
    data = pd.DataFrame({"otra_columna": [1, 2]}).to_json(
        orient="split"
    )

    with pytest.raises(ValueError, match="Faltan columnas requeridas"):
        actualizar_kpis(data)
import pandas as pd

from dashboard.dash_app import (
    actualizar_datos_filtrados,
)


def test_actualizar_datos_filtrados_returns_json():
    data = actualizar_datos_filtrados(
        "2024-01-01",
        "2025-12-31",
        "Todas",
        "Todos",
        "Todos",
        "Todos",
    )

    assert isinstance(data, str)
    assert len(data) > 0





def test_actualizar_lineas_returns_options():
    options, value = actualizar_lineas(
        "2024-01-01",
        "2025-12-31",
    )

    assert options
    assert options[0] == {"label": "Todas", "value": "Todas"}
    assert value == "Todas"


def test_actualizar_equipos_returns_options():
    options, value = actualizar_equipos(
        "Todas",
        "2024-01-01",
        "2025-12-31",
    )

    assert options
    assert options[0] == {"label": "Todos", "value": "Todos"}
    assert value == "Todos"


def test_actualizar_turnos_returns_options():
    options, value = actualizar_turnos(
        "Todos",
        "Todas",
        "2024-01-01",
        "2025-12-31",
    )

    assert options
    assert options[0] == {"label": "Todos", "value": "Todos"}
    assert value == "Todos"


def test_actualizar_operadores_returns_options():
    options, value = actualizar_operadores(
        "Todos",
        "Todos",
        "Todas",
        "2024-01-01",
        "2025-12-31",
    )

    assert options
    assert options[0] == {"label": "Todos", "value": "Todos"}
    assert value == "Todos"


def test_actualizar_datos_filtrados_with_specific_line():
    data = actualizar_datos_filtrados(
        "2024-01-01",
        "2025-12-31",
        "Línea 1",
        "Todos",
        "Todos",
        "Todos",
    )

    assert isinstance(data, str)
    assert len(data) > 0

def test_actualizar_kpis_produccion_is_positive():
    data = actualizar_datos_filtrados(
        "2024-01-01",
        "2025-12-31",
        "Todas",
        "Todos",
        "Todos",
        "Todos",
    )

    valores = actualizar_kpis(data)

    assert int(valores[0].replace(",", "")) > 0


def test_actualizar_kpis_returns_percentage_values():
    data = actualizar_datos_filtrados(
        "2024-01-01",
        "2025-12-31",
        "Todas",
        "Todos",
        "Todos",
        "Todos",
    )

    produccion, fpy, defectos, scrap = actualizar_kpis(data)

    assert produccion == "249,752"
    assert fpy.endswith("%")
    assert defectos.endswith("%")
    assert scrap.endswith("%")
