from dash import html

from dashboard.quality_performance_components import (
    crear_quality_performance,
)


def test_quality_performance_returns_section():
    componente = crear_quality_performance()

    assert isinstance(componente, html.Section)


def test_quality_performance_contains_expected_ids():
    componente = crear_quality_performance()

    ids = {
        nodo.id
        for nodo in componente.children
        if hasattr(nodo, "id") and nodo.id
    }

    assert "quality-fpy" not in ids


def test_quality_performance_contains_expected_metric_ids():
    componente = crear_quality_performance()

    contenido = str(componente)

    assert 'quality-fpy' in contenido
    assert 'quality-defect-rate' in contenido
    assert 'quality-scrap-rate' in contenido
    assert 'quality-rework-rate' in contenido


def test_quality_performance_contains_analysis_ids():
    componente = crear_quality_performance()

    contenido = str(componente)

    assert 'quality-pareto' in contenido
    assert 'quality-critical-lot' in contenido


def test_quality_performance_contains_expected_titles():
    componente = crear_quality_performance()

    contenido = str(componente)

    assert "Quality Performance" in contenido
    assert "Desempeño de calidad" in contenido
    assert "FPY" in contenido
    assert "Tasa de defectos" in contenido
    assert "Tasa de scrap" in contenido
    assert "Tasa de reproceso" in contenido


def test_quality_performance_uses_expected_section_class():
    componente = crear_quality_performance()

    assert componente.className == (
        "dashboard-section quality-performance"
    )


def test_quality_performance_pareto_has_empty_state_message():
    layout = crear_quality_performance()

    def encontrar_componente(component):
        if getattr(component, "id", None) == "quality-pareto":
            return component

        children = getattr(component, "children", None)

        if children is None:
            return None

        if not isinstance(children, (list, tuple)):
            children = [children]

        for child in children:
            encontrado = encontrar_componente(child)
            if encontrado is not None:
                return encontrado

        return None

    pareto = encontrar_componente(layout)

    assert pareto is not None
    assert pareto.children == (
        "Sin defectos en el período seleccionado."
    )
