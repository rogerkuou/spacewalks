import pytest
import sys

sys.path.insert(0, ".")
from eva_data_analysis import text_to_duration


test_data = [("11:30", 11.5), ("0:45", 0.75), ("2:15", 2.25)]


@pytest.mark.parametrize(
    "input_text, expected_output", test_data
)
def test_text_to_duration_value_corectness(input_text, expected_output):

    actual_output = text_to_duration(input_text)

    assert actual_output == expected_output
