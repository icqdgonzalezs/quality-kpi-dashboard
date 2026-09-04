from __future__ import annotations

from dash import html


def crear_quality_performance():
    return html.Section(
        [
            html.Div(
                [
                    html.H2(
                        "Quality Performance",
                        className="section-title",
                    ),
                    html.P(
                        "Desempeño de calidad y principales fuentes de defectos.",
                        className="section-subtitle",
                    ),
                ],
                className="section-header",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                "FPY",
                                className="quality-metric-label",
                            ),
                            html.Div(
                                id="quality-fpy",
                                className="quality-metric-value",
                            ),
                        ],
                        className="quality-metric-card",
                    ),
                    html.Div(
                        [
                            html.Div(
                                "Tasa de defectos",
                                className="quality-metric-label",
                            ),
                            html.Div(
                                id="quality-defect-rate",
                                className="quality-metric-value",
                            ),
                        ],
                        className="quality-metric-card",
                    ),
                    html.Div(
                        [
                            html.Div(
                                "Tasa de scrap",
                                className="quality-metric-label",
                            ),
                            html.Div(
                                id="quality-scrap-rate",
                                className="quality-metric-value",
                            ),
                        ],
                        className="quality-metric-card",
                    ),
                    html.Div(
                        [
                            html.Div(
                                "Tasa de reproceso",
                                className="quality-metric-label",
                            ),
                            html.Div(
                                id="quality-rework-rate",
                                className="quality-metric-value",
                            ),
                        ],
                        className="quality-metric-card",
                    ),
                ],
                className="quality-metrics-grid",
            ),
            html.Div(
                [
                    html.Div(
                        id="quality-pareto",
                        children="Sin defectos en el período seleccionado.",
                        className="quality-analysis-card",
                    ),
                    html.Div(
                        id="quality-critical-lot",
                        className="quality-analysis-card",
                    ),
                ],
                className="quality-analysis-grid",
            ),
        ],
        className="dashboard-section quality-performance",
    )
