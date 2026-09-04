from __future__ import annotations

from typing import Any


def formatear_kpis(kpis: dict[str, Any]) -> dict[str, str]:
    """Convierte el resultado del KPI Engine en valores de presentación."""
    required = {
        "fpy",
        "tasa_defectos",
        "tasa_scrap",
        "tasa_reproceso",
        "total_producidas",
        "total_defectuosas",
        "total_scrap",
        "total_reproceso",
    }

    faltantes = required - set(kpis)

    if faltantes:
        raise ValueError(
            "Faltan KPI requeridos: "
            + ", ".join(sorted(faltantes))
        )

    return {
        "produccion": f"{int(kpis['total_producidas']):,}",
        "fpy": f"{kpis['fpy']:.1%}",
        "defectos": f"{kpis['tasa_defectos']:.1%}",
        "scrap": f"{kpis['tasa_scrap']:.1%}",
        "reproceso": f"{kpis['tasa_reproceso']:.1%}",
        "total_defectuosas": f"{int(kpis['total_defectuosas']):,}",
        "total_scrap": f"{int(kpis['total_scrap']):,}",
        "total_reproceso": f"{int(kpis['total_reproceso']):,}",
    }
