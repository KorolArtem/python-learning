import pytest
from algorithms_and_data_structures.linked_list.linked_list import LinkedList

@pytest.fixture
def empty_list():
    return LinkedList()

@pytest.fixture
def single_list():
    ll = LinkedList()
    ll.append(67)
    return ll

@pytest.fixture
def populated_list():
    ll = LinkedList()
    for val in [10, 20, 30, 40, 50]:
        ll.append(val)
    return ll

def test_is_empty(empty_list, single_list, populated_list):
    assert empty_list.is_empty() is True
    assert single_list.is_empty() is False
    assert populated_list.is_empty() is False

def test_len(empty_list, single_list, populated_list):
    assert len(empty_list) == 0
    assert len(single_list) == 1
    assert len(populated_list) == 5

def test_bool(empty_list, single_list, populated_list):
    assert not empty_list
    assert single_list
    assert populated_list

def test_iter(empty_list, single_list, populated_list):
    assert list(empty_list) == []
    assert list(single_list) == [67]
    assert list(populated_list) == [10, 20, 30, 40, 50]
    
    iterator = iter(populated_list)
    assert next(iterator) == 10
    assert next(iterator) == 20

def test_contains(empty_list, single_list, populated_list):
    assert 67 not in empty_list
    assert 67 in single_list
    assert 99 not in single_list
    assert 10 in populated_list
    assert 30 in populated_list
    assert 50 in populated_list
    assert 99 not in populated_list

def test_repr(empty_list, single_list, populated_list):
    assert repr(empty_list) in ("None")
    assert repr(single_list) == "67 -> None"
    assert repr(populated_list) == "10 -> 20 -> 30 -> 40 -> 50 -> None"

def test_prepend(empty_list, single_list, populated_list):
    empty_list.prepend(1)
    assert list(empty_list) == [1]
    assert len(empty_list) == 1

    single_list.prepend(1)
    assert list(single_list) == [1, 67]
    assert len(single_list) == 2

    populated_list.prepend(1)
    assert list(populated_list) == [1, 10, 20, 30, 40, 50]
    assert len(populated_list) == 6

def test_append(empty_list, single_list, populated_list):
    empty_list.append(1)
    assert list(empty_list) == [1]
    assert len(empty_list) == 1

    single_list.append(1)
    assert list(single_list) == [67, 1]
    assert len(single_list) == 2

    populated_list.append(1)
    assert list(populated_list) == [10, 20, 30, 40, 50, 1]
    assert len(populated_list) == 6

def test_insert(empty_list, single_list, populated_list):
    empty_list.insert(0, 1)
    assert list(empty_list) == [1]

    single_list.insert(0, 1)
    assert list(single_list) == [1, 67]
    
    single_list.insert(2, 2)
    assert list(single_list) == [1, 67, 2]

    populated_list.insert(2, 25)
    assert list(populated_list) == [10, 20, 25, 30, 40, 50]

    populated_list.insert(6, 60)
    assert list(populated_list) == [10, 20, 25, 30, 40, 50, 60]

    populated_list.insert(-1, 99)
    assert list(populated_list) == [10, 20, 25, 30, 40, 50, 99, 60]

def test_insert_exceptions(empty_list, populated_list):
    with pytest.raises(IndexError):
        empty_list.insert(1, 1)
    
    with pytest.raises(IndexError):
        empty_list.insert(-1, 1)

    with pytest.raises(IndexError):
        populated_list.insert(10, 1)

    with pytest.raises(IndexError):
        populated_list.insert(-10, 1)

def test_pop_first(empty_list, single_list, populated_list):
    with pytest.raises(IndexError):
        empty_list.pop_first()

    assert single_list.pop_first() == 67
    assert list(single_list) == []
    assert len(single_list) == 0

    assert populated_list.pop_first() == 10
    assert list(populated_list) == [20, 30, 40, 50]
    assert len(populated_list) == 4

def test_pop_default(empty_list, single_list, populated_list):
    with pytest.raises(IndexError):
        empty_list.pop()

    assert single_list.pop() == 67
    assert list(single_list) == []
    assert len(single_list) == 0

    assert populated_list.pop() == 50
    assert list(populated_list) == [10, 20, 30, 40]
    assert len(populated_list) == 4

def test_pop_index(populated_list):
    assert populated_list.pop(0) == 10
    assert list(populated_list) == [20, 30, 40, 50]

    assert populated_list.pop(2) == 40
    assert list(populated_list) == [20, 30, 50]

    assert populated_list.pop(-1) == 50
    assert list(populated_list) == [20, 30]

    assert populated_list.pop(-2) == 20
    assert list(populated_list) == [30]

def test_pop_exceptions(empty_list, single_list, populated_list):
    with pytest.raises(IndexError):
        empty_list.pop(0)

    with pytest.raises(IndexError):
        single_list.pop(1)
        
    with pytest.raises(IndexError):
        single_list.pop(-2)

    with pytest.raises(IndexError):
        populated_list.pop(5)

    with pytest.raises(IndexError):
        populated_list.pop(-6)

def test_remove(empty_list, single_list, populated_list):
    with pytest.raises(ValueError):
        empty_list.remove(67)

    single_list.remove(67)
    assert list(single_list) == []

    populated_list.remove(10)
    assert list(populated_list) == [20, 30, 40, 50]

    populated_list.remove(30)
    assert list(populated_list) == [20, 40, 50]

    populated_list.remove(50)
    assert list(populated_list) == [20, 40]

    populated_list.append(20)
    populated_list.remove(20)
    assert list(populated_list) == [40, 20]

    with pytest.raises(ValueError):
        populated_list.remove(999)

def test_clear(empty_list, single_list, populated_list):
    empty_list.clear()
    assert list(empty_list) == []
    assert len(empty_list) == 0

    single_list.clear()
    assert list(single_list) == []
    assert len(single_list) == 0

    populated_list.clear()
    assert list(populated_list) == []
    assert len(populated_list) == 0

def test_get(empty_list, single_list, populated_list):
    assert single_list.get(0) == 67
    assert single_list.get(-1) == 67

    assert populated_list.get(0) == 10
    assert populated_list.get(2) == 30
    assert populated_list.get(4) == 50

    assert populated_list.get(-1) == 50
    assert populated_list.get(-3) == 30
    assert populated_list.get(-5) == 10

def test_getitem(single_list, populated_list):
    assert single_list[0] == 67
    assert single_list[-1] == 67

    assert populated_list[0] == 10
    assert populated_list[2] == 30
    assert populated_list[4] == 50

    assert populated_list[-1] == 50
    assert populated_list[-3] == 30
    assert populated_list[-5] == 10

def test_get_exceptions(empty_list, single_list, populated_list):
    with pytest.raises(IndexError):
        empty_list.get(0)
    with pytest.raises(IndexError):
        _ = empty_list[0]

    with pytest.raises(IndexError):
        single_list.get(1)
    with pytest.raises(IndexError):
        single_list.get(-2)

    with pytest.raises(IndexError):
        populated_list.get(5)
    with pytest.raises(IndexError):
        populated_list.get(-6)

def test_find(empty_list, single_list, populated_list):
    assert empty_list.find(67) in (-1, None)

    assert single_list.find(67) == 0
    assert single_list.find(99) in (-1, None)

    assert populated_list.find(10) == 0
    assert populated_list.find(30) == 2
    assert populated_list.find(50) == 4
    
    populated_list.append(30)
    assert populated_list.find(30) == 2
    
    assert populated_list.find(99) in (-1, None)

def test_tail_append_prepend(empty_list):
    empty_list.prepend(10)
    assert empty_list.tail.value == 10
    assert empty_list.head is empty_list.tail

    empty_list.prepend(20)
    assert empty_list.tail.value == 10

    empty_list.append(30)
    assert empty_list.tail.value == 30

def test_tail_insert(empty_list):
    empty_list.insert(0, 10)
    assert empty_list.tail.value == 10

    empty_list.insert(1, 20)
    assert empty_list.tail.value == 20

    empty_list.insert(1, 15)
    assert empty_list.tail.value == 20

def test_tail_pop_first_and_clear(empty_list):
    empty_list.append(10)
    empty_list.append(20)
    
    empty_list.pop_first()
    assert empty_list.tail.value == 20
    
    empty_list.pop_first()
    assert empty_list.tail is None

    empty_list.append(10)
    empty_list.clear()
    assert empty_list.tail is None

def test_tail_pop_index(empty_list):
    empty_list.append(10)
    empty_list.append(20)
    empty_list.append(30)

    empty_list.pop(1)
    assert empty_list.tail.value == 30

    empty_list.pop(-1)
    assert empty_list.tail.value == 10

    empty_list.pop(0)
    assert empty_list.tail is None

def test_tail_remove_value(empty_list):
    empty_list.append(10)
    empty_list.append(20)
    empty_list.append(30)

    empty_list.remove(20)
    assert empty_list.tail.value == 30

    empty_list.remove(30)
    assert empty_list.tail.value == 10

    empty_list.remove(10)
    assert empty_list.tail is None