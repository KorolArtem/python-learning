import pytest
from algorithms_and_data_structures.linked_list.linked_list import LinkedList
from algorithms_and_data_structures.linked_list.reverse_linked_list import reverse_linked_list

def test_reverse_empty_list():
    ll = LinkedList()
    reversed_ll = reverse_linked_list(ll)
    
    assert list(reversed_ll) == []
    assert reversed_ll.head is None
    assert reversed_ll.tail is None

def test_reverse_single_element():
    ll = LinkedList()
    ll.append(10)
    reversed_ll = reverse_linked_list(ll)
    
    assert list(reversed_ll) == [10]
    assert reversed_ll.head.value == 10
    assert reversed_ll.tail.value == 10
    assert reversed_ll.head is reversed_ll.tail
    assert reversed_ll.tail.next is None

def test_reverse_two_elements():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    reversed_ll = reverse_linked_list(ll)
    
    assert list(reversed_ll) == [20, 10]
    assert reversed_ll.head.value == 20
    assert reversed_ll.tail.value == 10
    assert reversed_ll.tail.next is None

def test_reverse_multiple_elements():
    ll = LinkedList()
    for i in [10, 20, 30, 40, 50]:
        ll.append(i)
        
    reversed_ll = reverse_linked_list(ll)
    
    assert list(reversed_ll) == [50, 40, 30, 20, 10]
    assert reversed_ll.head.value == 50
    assert reversed_ll.tail.value == 10
    assert reversed_ll.tail.next is None

def test_mutations_after_reverse():
    ll = LinkedList()
    for i in [1, 2, 3]:
        ll.append(i)
        
    reverse_linked_list(ll)
    
    ll.append(4)
    ll.prepend(0)
    
    assert list(ll) == [0, 3, 2, 1, 4]
    assert ll.head.value == 0
    assert ll.tail.value == 4
    assert len(ll) == 5