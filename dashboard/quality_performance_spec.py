from __future__ import annotations


QUALITY_PERFORMANCE_SPEC = {
    "title": "Quality Performance",
    "description": (
        "Vista de desempeño de calidad basada en producción, FPY, "
        "defectos, scrap, reproceso y distribución de defectos."
    ),
    "metrics": {
        "production": {
            "label": "Producción",
            "source": "src.kpis.calcular_kpis_globales",
            "field": "total_producidas",
            "format": "integer",
        },
        "fpy": {
            "label": "FPY",
            "source": "src.kpis.calcular_kpis_globales",
            "field": "fpy",
            "format": "percentage",
        },
        "defect_rate": {
            "label": "Tasa de defectos",
            "source": "src.kpis.calcular_kpis_globales",
            "field": "tasa_defectos",
            "format": "percentage",
        },
        "scrap_rate": {
            "label": "Tasa de scrap",
            "source": "src.kpis.calcular_kpis_globales",
            "field": "tasa_scrap",
            "format": "percentage",
        },
        "rework_rate": {
            "label": "Tasa de reproceso",
            "source": "src.kpis.calcular_kpis_globales",
            "field": "tasa_reproceso",
            "format": "percentage",
        },
    },
    "analysis": {
        "pareto": {
            "source": "src.kpis.calcular_pareto",
            "purpose": "Priorizar defectos por frecuencia acumulada.",
        },
        "critical_lot": {
            "source": "src.kpis.identificar_lote_critico",
            "purpose": "Identificar el lote con mayor tasa de defectos.",
        },
    },
}


def obtener_quality_performance_spec() -> dict:
    return QUALITY_PERFORMANCE_SPEC.copy()
