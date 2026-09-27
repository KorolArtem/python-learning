import pytest
from algorithms_and_data_structures.stack.reverse_polish_notation import calculate_expression

def test_basic_rpn_operations():
    
    assert calculate_expression("2 1 +") == 3
    
    assert calculate_expression("4 13 5 / +") == 6
    
    assert calculate_expression("10, 6, 9, 3, +, -11, *, /, *, 17, +, 5, +") == 22

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate_expression("4 0 /")

@pytest.mark.parametrize(
    "bad_expression",
    [
        "1 +",
        "1 2 3 +",
        "",
    ],
)
def test_invalid_expression(bad_expression):
    with pytest.raises(ValueError):
        calculate_expression(bad_expression)