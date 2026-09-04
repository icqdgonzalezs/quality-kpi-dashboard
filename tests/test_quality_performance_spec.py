from dashboard.quality_performance_spec import (
    obtener_quality_performance_spec,
)


def test_quality_performance_spec_has_expected_title():
    spec = obtener_quality_performance_spec()

    assert spec["title"] == "Quality Performance"


def test_quality_performance_spec_has_required_metrics():
    spec = obtener_quality_performance_spec()

    assert set(spec["metrics"]) == {
        "production",
        "fpy",
        "defect_rate",
        "scrap_rate",
        "rework_rate",
    }


def test_quality_performance_metrics_use_kpi_engine():
    spec = obtener_quality_performance_spec()

    for metric in spec["metrics"].values():
        assert metric["source"] == "src.kpis.calcular_kpis_globales"


def test_quality_performance_has_required_analyses():
    spec = obtener_quality_performance_spec()

    assert set(spec["analysis"]) == {
        "pareto",
        "critical_lot",
    }


def test_quality_performance_analysis_uses_src_kpis():
    spec = obtener_quality_performance_spec()

    assert (
        spec["analysis"]["pareto"]["source"]
        == "src.kpis.calcular_pareto"
    )

    assert (
        spec["analysis"]["critical_lot"]["source"]
        == "src.kpis.identificar_lote_critico"
    )


def test_quality_performance_spec_returns_independent_top_level_dict():
    spec = obtener_quality_performance_spec()

    spec["title"] = "Modified"

    fresh_spec = obtener_quality_performance_spec()

    assert fresh_spec["title"] == "Quality Performance"
