import pandas as pd
import pytest

import dashboard.data_loader as data_loader


def test_cargar_datos_returns_dataframe_and_config():
    df, config = data_loader.cargar_datos()

    assert isinstance(df, pd.DataFrame)
    assert isinstance(config, dict)
    assert not df.empty


def test_cargar_datos_parses_fecha_column():
    df, _ = data_loader.cargar_datos()

    assert "fecha" in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df["fecha"])


def test_cargar_datos_raises_when_dataset_is_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(
        data_loader,
        "DATA_PATH",
        tmp_path / "missing.csv",
    )

    with pytest.raises(FileNotFoundError, match="No existe el dataset"):
        data_loader.cargar_datos()


def test_cargar_datos_raises_when_config_is_missing(monkeypatch, tmp_path):
    dataset_path = tmp_path / "data.csv"

    pd.DataFrame(
        {
            "fecha": ["2024-01-01"],
            "valor": [1],
        }
    ).to_csv(dataset_path, index=False)

    monkeypatch.setattr(
        data_loader,
        "DATA_PATH",
        dataset_path,
    )
    monkeypatch.setattr(
        data_loader,
        "QUALITY_CONFIG_PATH",
        tmp_path / "missing.yaml",
    )

    with pytest.raises(
        FileNotFoundError,
        match="No existe la configuración",
    ):
        data_loader.cargar_datos()


def test_cargar_datos_handles_empty_yaml(monkeypatch, tmp_path):
    dataset_path = tmp_path / "data.csv"
    config_path = tmp_path / "config.yaml"

    pd.DataFrame(
        {
            "fecha": ["2024-01-01"],
            "valor": [1],
        }
    ).to_csv(dataset_path, index=False)

    config_path.write_text("", encoding="utf-8")

    monkeypatch.setattr(
        data_loader,
        "DATA_PATH",
        dataset_path,
    )
    monkeypatch.setattr(
        data_loader,
        "QUALITY_CONFIG_PATH",
        config_path,
    )

    df, config = data_loader.cargar_datos()

    assert isinstance(df, pd.DataFrame)
    assert config == {}


def test_cargar_datos_does_not_require_fecha_column(
    monkeypatch,
    tmp_path,
):
    dataset_path = tmp_path / "data.csv"
    config_path = tmp_path / "config.yaml"

    pd.DataFrame(
        {
            "valor": [1, 2],
        }
    ).to_csv(dataset_path, index=False)

    config_path.write_text(
        "test: true\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        data_loader,
        "DATA_PATH",
        dataset_path,
    )
    monkeypatch.setattr(
        data_loader,
        "QUALITY_CONFIG_PATH",
        config_path,
    )

    df, config = data_loader.cargar_datos()

    assert "fecha" not in df.columns
    assert config["test"] is True
