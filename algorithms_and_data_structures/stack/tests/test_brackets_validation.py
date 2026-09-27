import pytest
from algorithms_and_data_structures.stack.brackets_validation import validate_brackets

@pytest.mark.parametrize(
    "sequence, expected",
    [
        ("", True),
        ("()", True),
        ("()[]{}", True),
        ("{[()]}", True),
        ("([)]", False),
        ("(", False),
        (")", False),
        ("{[}", False),
        (["(", "{", "}", ")"], True),
    ],
)
def test_validate_brackets(sequence, expected):
    assert validate_brackets(sequence) == expected

def test_invalid_type():
    with pytest.raises(TypeError):
        validate_brackets(12345)