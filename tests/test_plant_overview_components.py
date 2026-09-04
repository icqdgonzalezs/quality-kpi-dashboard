from dash import html

from dashboard.plant_overview_components import (
    crear_plant_overview,
    crear_tarjeta_equipo,
)


def test_crear_tarjeta_equipo_tiene_id_pattern():
    tarjeta = crear_tarjeta_equipo("L1-M01")

    assert tarjeta.id == {
        "type": "plant-equipment-card",
        "equipment": "L1-M01",
    }
    assert tarjeta.className == "plant-equipment-card"


def test_crear_tarjeta_equipo_contiene_elementos_esperados():
    tarjeta = crear_tarjeta_equipo("L1-M01")

    assert len(tarjeta.children) == 4

    assert tarjeta.children[0].children == "L1-M01"
    assert tarjeta.children[0].className == "plant-equipment-id"

    assert tarjeta.children[1].children == "—"
    assert tarjeta.children[1].className == (
        "plant-equipment-defect-rate"
    )

    assert tarjeta.children[2].children == "SIN DATOS"
    assert tarjeta.children[2].className == (
        "plant-equipment-status"
    )

    assert tarjeta.children[3].children == (
        "0 lotes · 0 defectuosas"
    )
    assert tarjeta.children[3].className == (
        "plant-equipment-detail"
    )


def test_crear_plant_overview_tiene_ids_principales():
    component = crear_plant_overview(
        ["L1-M01", "L1-M02"]
    )

    assert component.id == "plant-overview"
    assert component.className == (
        "dashboard-section plant-overview"
    )

    grid = component.children[3]

    assert grid.id == "plant-equipment-grid"
    assert grid.className == "plant-equipment-grid"


def test_crear_plant_overview_crea_una_tarjeta_por_equipo():
    component = crear_plant_overview(
        ["L1-M01", "L1-M02", "L2-M01"]
    )

    grid = component.children[3]

    assert len(grid.children) == 3
    assert [
        child.id["equipment"]
        for child in grid.children
    ] == [
        "L1-M01",
        "L1-M02",
        "L2-M01",
    ]


def test_crear_plant_overview_sin_equipos_no_falla():
    component = crear_plant_overview()

    assert component.id == "plant-overview"

    grid = component.children[3]

    assert grid.children == []
