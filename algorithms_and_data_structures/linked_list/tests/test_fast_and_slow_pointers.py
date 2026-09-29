import pytest
from algorithms_and_data_structures.linked_list.linked_list import LinkedList
from algorithms_and_data_structures.linked_list.fast_and_slow_pointers import fast_and_slow_pointers

def test_middle_odd_length():
    ll = LinkedList()
    for i in [1, 2, 3, 4, 5]:
        ll.append(i)
    
    assert fast_and_slow_pointers(ll) == 3

def test_middle_even_length():
    ll = LinkedList()
    for i in [1, 2, 3, 4]:
        ll.append(i)

    assert fast_and_slow_pointers(ll) == 3

def test_middle_single_element():
    ll = LinkedList()
    ll.append(67)
    
    assert fast_and_slow_pointers(ll) == 67

def test_middle_empty_list():
    ll = LinkedList()
    
    with pytest.raises(ValueError):
        fast_and_slow_pointers(ll)