import pytest
import sys 
sys.path.insert(0, ".")
from eva_data_analysis import text_to_duration

def test_text_to_duration_value_corectness():
    input_text = "11:30"
    expected_output = 11.5

    actual_output = text_to_duration(input_text)
    
    assert actual_output == expected_output

