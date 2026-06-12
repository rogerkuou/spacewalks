import pytest
import sys
import pandas as pd

sys.path.insert(0, ".")
from eva_data_analysis import (
    text_to_duration,
    read_json_to_clean_dataframe,
    plot_eva_durations,
    compute_durations,
)


@pytest.fixture(scope="module")
def sample_dataframe():
    df = read_json_to_clean_dataframe("data/eva_data.json")
    eva_df = compute_durations(df)
    return eva_df


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("11:30", 11.5),
        ("0:45", 0.75),
        ("2:15", 2.25),
    ],
)
def test_text_to_duration_value_corectness(input_text, expected_output):
    actual_output = text_to_duration(input_text)

    assert actual_output == expected_output


def test_read_json_to_clean_dataframe():
    df = read_json_to_clean_dataframe("data/eva_data.json")
    # check shape
    assert df.shape == (330, 7)
    # check no na values in duration and date columns
    assert df["duration"].isna().sum() == 0
    assert df["date"].isna().sum() == 0
    # check date sorting
    assert df["date"].is_monotonic_increasing


def test_plot_eva_durations(sample_dataframe, tmp_path):
    graph_file = tmp_path / "test_graph.png"
    plot_eva_durations(graph_file, sample_dataframe)
    assert graph_file.exists()
