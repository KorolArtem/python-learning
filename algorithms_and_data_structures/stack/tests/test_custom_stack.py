import pytest
from algorithms_and_data_structures.stack.custom_stack import Stack

def test_get_min_constant_time():
    s = Stack()
    s.push(5)
    assert s.get_min() == 5
    s.push(3)
    assert s.get_min() == 3
    s.push(7)
    assert s.get_min() == 3
    s.push(3)
    assert s.get_min() == 3

    assert s.pop() == 3
    assert s.get_min() == 3
    assert s.pop() == 7
    assert s.get_min() == 3
    assert s.pop() == 3
    assert s.get_min() == 5

def test_custom_stack_type_error():
    s = Stack()
    with pytest.raises(TypeError):
        s.push("not a number")

def test_custom_stack_empty_exceptions():
    s = Stack()
    with pytest.raises(IndexError):
        s.top()
    with pytest.raises(IndexError):
        s.pop()
    with pytest.raises(IndexError):
        s.get_min()