"""Sistema visual centralizado de Industrial KPI Intelligence."""

from __future__ import annotations


# ---------------------------------------------------------------------
# PALETA INDUSTRIAL
# ---------------------------------------------------------------------

COLORS = {
    # Interfaz
    "background": "#0B1220",
    "surface": "#111827",
    "surface_alt": "#182234",
    "border": "#263247",
    "text": "#E5E7EB",
    "text_muted": "#94A3B8",

    # Semántica operacional
    "normal": "#22C55E",
    "warning": "#F59E0B",
    "critical": "#EF4444",
    "info": "#38BDF8",
    "reference": "#64748B",

    # Analítica
    "primary": "#38BDF8",
    "secondary": "#8B5CF6",
    "accent": "#14B8A6",
}


# ---------------------------------------------------------------------
# ESTADOS
# ---------------------------------------------------------------------

STATUS_SYMBOLS = {
    "NORMAL": "●",
    "WATCH": "▲",
    "PRIORITY": "■",
    "NO DATA": "○",
}


STATUS_COLORS = {
    "NORMAL": COLORS["normal"],
    "WATCH": COLORS["warning"],
    "PRIORITY": COLORS["critical"],
    "NO DATA": COLORS["reference"],
}


# ---------------------------------------------------------------------
# CONFIGURACIÓN PLOTLY
# ---------------------------------------------------------------------

PLOTLY_FONT = "Arial"

PLOTLY_LAYOUT = {
    "font": {
        "family": PLOTLY_FONT,
        "color": "#1F2937",
    },
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "margin": {
        "l": 55,
        "r": 25,
        "t": 55,
        "b": 50,
    },
    "hoverlabel": {
        "font": {
            "family": PLOTLY_FONT,
        },
    },
}


# ---------------------------------------------------------------------
# COLORES PARA GRÁFICOS
# ---------------------------------------------------------------------

CHART_COLORS = {
    "trend": COLORS["primary"],
    "pareto_bar": COLORS["primary"],
    "pareto_line": COLORS["warning"],
    "specification": COLORS["critical"],
    "nominal": COLORS["primary"],
    "mean": COLORS["warning"],
}


def get_status_color(status: str) -> str:
    """Devuelve el color asociado a un estado operacional."""
    return STATUS_COLORS.get(
        status,
        COLORS["reference"],
    )


def get_status_symbol(status: str) -> str:
    """Devuelve el símbolo asociado a un estado operacional."""
    return STATUS_SYMBOLS.get(
        status,
        STATUS_SYMBOLS["NO DATA"],
    )
