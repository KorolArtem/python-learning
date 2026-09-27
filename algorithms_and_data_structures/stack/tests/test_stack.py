import pytest
from algorithms_and_data_structures.stack.stack import Stack

def test_push_and_top():
    s = Stack()
    s.push(10)
    assert s.top() == 10
    s.push(20)
    assert s.top() == 20

def test_pop():
    s = Stack()
    s.push(1)
    s.push(2)
    assert s.pop() == 2
    assert s.pop() == 1
    assert s.is_empty() is True

def test_empty_stack_exceptions():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

    with pytest.raises(IndexError):
        s.top()

def test_clear():
    s = Stack()
    s.push(1)
    s.push(2)
    s.clear()
    assert s.is_empty() is True