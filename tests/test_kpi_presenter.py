import pytest

from dashboard.kpi_presenter import formatear_kpis


@pytest.fixture
def kpis():
    return {
        "fpy": 0.9536540247925942,
        "tasa_defectos": 0.04634597520740575,
        "tasa_scrap": 0.014134020948781191,
        "tasa_reproceso": 0.03221195425862455,
        "total_producidas": 249752,
        "total_defectuosas": 11575,
        "total_scrap": 3530,
        "total_reproceso": 8045,
    }


def test_formatear_kpis_returns_all_expected_keys(kpis):
    resultado = formatear_kpis(kpis)

    expected = {
        "produccion",
        "fpy",
        "defectos",
        "scrap",
        "reproceso",
        "total_defectuosas",
        "total_scrap",
        "total_reproceso",
    }

    assert set(resultado) == expected


def test_formatear_kpis_formats_values_correctly(kpis):
    resultado = formatear_kpis(kpis)

    assert resultado["produccion"] == "249,752"
    assert resultado["fpy"] == "95.4%"
    assert resultado["defectos"] == "4.6%"
    assert resultado["scrap"] == "1.4%"
    assert resultado["reproceso"] == "3.2%"
    assert resultado["total_defectuosas"] == "11,575"
    assert resultado["total_scrap"] == "3,530"
    assert resultado["total_reproceso"] == "8,045"


def test_formatear_kpis_raises_when_required_key_is_missing(kpis):
    del kpis["fpy"]

    with pytest.raises(ValueError, match="Faltan KPI requeridos"):
        formatear_kpis(kpis)


def test_formatear_kpis_accepts_integer_totals_and_float_rates():
    kpis = {
        "fpy": 1.0,
        "tasa_defectos": 0.0,
        "tasa_scrap": 0.0,
        "tasa_reproceso": 0.0,
        "total_producidas": 1000,
        "total_defectuosas": 0,
        "total_scrap": 0,
        "total_reproceso": 0,
    }

    resultado = formatear_kpis(kpis)

    assert resultado["produccion"] == "1,000"
    assert resultado["fpy"] == "100.0%"
    assert resultado["defectos"] == "0.0%"
    assert resultado["scrap"] == "0.0%"
    assert resultado["reproceso"] == "0.0%"
