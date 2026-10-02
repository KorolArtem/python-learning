import pytest
from algorithms_and_data_structures.doubly_linked_list.doubly_linked_list import DoublyLinkedList

def assert_state(ll, expected):
    assert list(ll) == expected
    assert list(reversed(ll)) == expected[::-1]
    assert len(ll) == len(expected)

@pytest.fixture
def empty_list():
    return DoublyLinkedList()

@pytest.fixture
def single_list():
    ll = DoublyLinkedList()
    ll.append(67)
    return ll

@pytest.fixture
def populated_list():
    ll = DoublyLinkedList()
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

def test_reversed(empty_list, single_list, populated_list):
    assert list(reversed(empty_list)) == []
    assert list(reversed(single_list)) == [67]
    assert list(reversed(populated_list)) == [50, 40, 30, 20, 10]

def test_contains(empty_list, single_list, populated_list):
    assert 67 not in empty_list
    assert 67 in single_list
    assert 99 not in single_list
    assert 30 in populated_list
    assert 99 not in populated_list

def test_prepend(empty_list, single_list, populated_list):
    empty_list.prepend(1)
    assert_state(empty_list, [1])
    assert empty_list.head is empty_list.tail

    single_list.prepend(1)
    assert_state(single_list, [1, 67])

    populated_list.prepend(1)
    assert_state(populated_list, [1, 10, 20, 30, 40, 50])

def test_append(empty_list, single_list, populated_list):
    empty_list.append(1)
    assert_state(empty_list, [1])
    assert empty_list.head is empty_list.tail

    single_list.append(1)
    assert_state(single_list, [67, 1])

    populated_list.append(1)
    assert_state(populated_list, [10, 20, 30, 40, 50, 1])

def test_insert(empty_list, single_list, populated_list):
    empty_list.insert(0, 1)
    assert_state(empty_list, [1])

    single_list.insert(0, 1)
    assert_state(single_list, [1, 67])

    single_list.insert(2, 2)
    assert_state(single_list, [1, 67, 2])

    populated_list.insert(2, 25)
    assert_state(populated_list, [10, 20, 25, 30, 40, 50])

    populated_list.insert(6, 60)
    assert_state(populated_list, [10, 20, 25, 30, 40, 50, 60])

    populated_list.insert(-1, 99)
    assert_state(populated_list, [10, 20, 25, 30, 40, 50, 99, 60])

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
    assert_state(single_list, [])
    assert single_list.head is None
    assert single_list.tail is None

    assert populated_list.pop_first() == 10
    assert_state(populated_list, [20, 30, 40, 50])
    assert populated_list.head.prev is None

def test_pop_last(empty_list, single_list, populated_list):
    with pytest.raises(IndexError):
        empty_list.pop_last()

    assert single_list.pop_last() == 67
    assert_state(single_list, [])
    assert single_list.head is None
    assert single_list.tail is None

    assert populated_list.pop_last() == 50
    assert_state(populated_list, [10, 20, 30, 40])
    assert populated_list.tail.next is None

def test_pop(empty_list, single_list, populated_list):
    with pytest.raises(IndexError):
        empty_list.pop(0)

    assert single_list.pop(0) == 67
    assert_state(single_list, [])

    assert populated_list.pop(2) == 30
    assert_state(populated_list, [10, 20, 40, 50])

    assert populated_list.pop(-1) == 50
    assert_state(populated_list, [10, 20, 40])

def test_pop_default(empty_list, populated_list):
    with pytest.raises(IndexError):
        empty_list.pop()
    assert populated_list.pop() == 50
    assert_state(populated_list, [10, 20, 30, 40])

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
    assert_state(single_list, [])

    populated_list.remove(10)
    assert_state(populated_list, [20, 30, 40, 50])

    populated_list.remove(30)
    assert_state(populated_list, [20, 40, 50])

    populated_list.remove(50)
    assert_state(populated_list, [20, 40])

    populated_list.append(20)
    populated_list.remove(20)
    assert_state(populated_list, [40, 20])

    with pytest.raises(ValueError):
        populated_list.remove(999)

def test_remove_node(single_list, populated_list):
    node_to_remove = single_list.head
    val = single_list.remove_node(node_to_remove)
    assert val == 67
    assert_state(single_list, [])

    mid_node = populated_list.head.next.next
    val = populated_list.remove_node(mid_node)
    assert val == 30
    assert_state(populated_list, [10, 20, 40, 50])

    last_node = populated_list.tail
    val = populated_list.remove_node(last_node)
    assert val == 50
    assert_state(populated_list, [10, 20, 40])

def test_clear(empty_list, single_list, populated_list):
    empty_list.clear()
    assert_state(empty_list, [])

    single_list.clear()
    assert_state(single_list, [])
    assert single_list.head is None
    assert single_list.tail is None

    populated_list.clear()
    assert_state(populated_list, [])
    assert populated_list.head is None
    assert populated_list.tail is None

def test_get(single_list, populated_list):
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
    with pytest.raises(ValueError):
        empty_list.find(67)

    assert single_list.find(67) == 0

    with pytest.raises(ValueError):
        single_list.find(99)

    assert populated_list.find(10) == 0
    assert populated_list.find(30) == 2
    assert populated_list.find(50) == 4

    populated_list.append(30)
    assert populated_list.find(30) == 2

    with pytest.raises(ValueError):
        populated_list.find(99)

def test_repr(empty_list, single_list, populated_list):
    assert repr(single_list) == "67 <-> None"
    assert repr(populated_list) == "10 <-> 20 <-> 30 <-> 40 <-> 50 <-> None"
    assert repr(empty_list) == "None"

def test_remove_node_after_clear(single_list):
    node = single_list.head
    single_list.clear()
    with pytest.raises(ValueError, match="does not belong"):
        single_list.remove_node(node)

def test_remove_node_errors(single_list, populated_list):
    with pytest.raises(ValueError, match="does not belong"):
        populated_list.remove_node(single_list.head)
    with pytest.raises(TypeError):
        populated_list.remove_node("not a node")

def test_get_from_tail_side(populated_list):
    assert populated_list.get(3) == 40
    assert populated_list.get(-2) == 40

def test_pop_from_tail_side(populated_list):
    assert populated_list.pop(3) == 40
    assert_state(populated_list, [10, 20, 30, 50])

def test_insert_from_tail_side(populated_list):
    populated_list.insert(3, 35)
    assert_state(populated_list, [10, 20, 30, 35, 40, 50])