from pathlib import Path

import pandas as pd

from src.data_generator import (
    DEFECT_TYPE_DIST,
    GENERATOR_CONFIG,
    generate_production_data,
)


def test_generator_config_contains_required_sections():
    required = {
        "generation",
        "shift_effects",
        "generation_limits",
        "scrap_rework",
        "production_per_shift",
        "base_defect_rate_pct",
        "defect_type_distribution",
        "drift_events",
        "product_effect",
    }
    assert required.issubset(GENERATOR_CONFIG)


def test_defect_distributions_sum_to_one():
    for distribution in DEFECT_TYPE_DIST.values():
        assert abs(sum(distribution.values()) - 1.0) < 1e-9


def test_generated_dataset_has_expected_structure():
    df = generate_production_data()

    required_columns = {
        "timestamp",
        "date",
        "year",
        "month",
        "week",
        "shift",
        "operator_id",
        "line_id",
        "equipment_id",
        "equipment_type",
        "product_id",
        "units_produced",
        "units_defective",
        "units_scrap",
        "units_rework",
        "defect_type",
    }

    assert required_columns.issubset(df.columns)
    assert len(df) > 0


def test_generated_dataset_respects_core_constraints():
    df = generate_production_data()

    assert (df["units_produced"] >= 0).all()
    assert (df["units_defective"] <= df["units_produced"]).all()
    assert (df["units_scrap"] <= df["units_defective"]).all()
    assert (df["units_rework"] <= df["units_defective"]).all()
    assert (
        df["units_defective"]
        == df["units_scrap"] + df["units_rework"]
    ).all()


def test_generated_dataset_is_reproducible():
    first = generate_production_data()
    second = generate_production_data()

    pd.testing.assert_frame_equal(first, second)


def test_generator_config_file_exists():
    config_path = Path("config/generator_config.yaml")
    assert config_path.exists()


def test_main_creates_output_file(tmp_path, monkeypatch):
    import src.data_generator as generator

    monkeypatch.chdir(tmp_path)
    generator.main()

    output_path = tmp_path / "data" / "raw" / "synthetic_production_data.csv"

    assert output_path.exists()

    df = pd.read_csv(output_path)

    assert not df.empty
    assert len(df.columns) == 16
