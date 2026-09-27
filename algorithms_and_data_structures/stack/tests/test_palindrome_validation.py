import pytest
from algorithms_and_data_structures.stack.palindrome_validation import validate_palindrome

@pytest.mark.parametrize(
    "word, expected",
    [
        ("radar", True),
        ("noon", True),
        ("a", True),
        ("abcba", True),
        ("hello", False),
        ("ab", False),
        (["r", "a", "d", "a", "r"], True),
    ],
)
def test_validate_palindrome(word, expected):
    assert validate_palindrome(word) == expected

def test_empty_palindrome_raises_error():
    with pytest.raises(ValueError):
        validate_palindrome("")