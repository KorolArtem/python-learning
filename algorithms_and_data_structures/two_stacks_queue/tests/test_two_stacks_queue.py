import pytest
from algorithms_and_data_structures.two_stacks_queue.two_stacks_queue import Queue

@pytest.fixture
def empty_queue():
    return Queue()

@pytest.fixture
def populated_queue():
    q = Queue()
    for i in [10, 20, 30, 40, 50]:
        q.enqueue(i)
    return q

def test_is_empty(empty_queue, populated_queue):
    assert empty_queue.is_empty() is True
    assert populated_queue.is_empty() is False

def test_bool(empty_queue, populated_queue):
    assert not empty_queue
    assert populated_queue

def test_enqueue(empty_queue):
    empty_queue.enqueue(1)
    assert empty_queue.is_empty() is False
    assert len(empty_queue) == 1
    
    empty_queue.enqueue(2)
    assert len(empty_queue) == 2

def test_dequeue(populated_queue):
    assert populated_queue.dequeue() == 10
    assert len(populated_queue) == 4
    
    assert populated_queue.dequeue() == 20
    assert populated_queue.dequeue() == 30
    assert populated_queue.dequeue() == 40
    assert populated_queue.dequeue() == 50
    
    assert populated_queue.is_empty() is True

def test_peek(populated_queue):
    assert populated_queue.peek() == 10
    assert len(populated_queue) == 5
    
    populated_queue.dequeue()
    assert populated_queue.peek() == 20
    assert len(populated_queue) == 4

def test_alternating_operations(empty_queue):
    empty_queue.enqueue(1)
    empty_queue.enqueue(2)
    
    assert empty_queue.dequeue() == 1
    
    empty_queue.enqueue(3)
    empty_queue.enqueue(4)
    
    assert empty_queue.dequeue() == 2
    assert empty_queue.peek() == 3
    assert empty_queue.dequeue() == 3
    assert empty_queue.dequeue() == 4
    assert empty_queue.is_empty() is True

def test_exceptions(empty_queue):
    with pytest.raises(IndexError):
        empty_queue.dequeue()
        
    with pytest.raises(IndexError):
        empty_queue.peek()

def test_len_empty_and_mutations(empty_queue):
    assert len(empty_queue) == 0
    empty_queue.enqueue(100)
    assert len(empty_queue) == 1
    empty_queue.dequeue()
    assert len(empty_queue) == 0

def test_repr(empty_queue, populated_queue):
    assert repr(empty_queue) == "Queue(in_stack_size=0, out_stack_size=0)"
    
    assert repr(populated_queue) == "Queue(in_stack_size=5, out_stack_size=0)"
    
    populated_queue.peek()
    assert repr(populated_queue) == "Queue(in_stack_size=0, out_stack_size=5)"

def test_str_does_not_crash(populated_queue):
    result = str(populated_queue)
    assert isinstance(result, str)

def test_str(empty_queue, populated_queue):
    assert str(empty_queue) == "Queue()"
    assert str(populated_queue) == "Queue(10 -> 20 -> 30 -> 40 -> 50)"

def test_iter(empty_queue, populated_queue):
    assert list(empty_queue) == []
    assert list(populated_queue) == [10, 20, 30, 40, 50]

def test_iter_with_both_stacks_filled(populated_queue):
    populated_queue.dequeue()
    populated_queue.enqueue(60)
    assert list(populated_queue) == [20, 30, 40, 50, 60]