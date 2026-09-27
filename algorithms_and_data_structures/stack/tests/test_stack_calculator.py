import pytest
from algorithms_and_data_structures.stack.stack_calculator import evaluate_expression

@pytest.mark.parametrize(
    "expr, expected",
    [
        ("2 + 2", 4.0),
        ("2 + 3 * 4", 14.0),
        ("(2 + 3) * 4", 20.0),
        ("10 - 2 * 3 + 4 / 2", 6.0),
        ("( ( 2 + 3 ) * 2 ) / 5", 2.0),
    ],
)
def test_valid_expressions(expr, expected):
    assert evaluate_expression(expr) == pytest.approx(expected)

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        evaluate_expression("10 / (2 - 2)")

def test_mismatched_brackets():
    with pytest.raises(ValueError):
        evaluate_expression("(2 + 3")

def test_invalid_tokens():
    with pytest.raises(ValueError):
        evaluate_expression("2 + a")