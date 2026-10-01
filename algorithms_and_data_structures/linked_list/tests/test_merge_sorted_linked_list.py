import pytest
from algorithms_and_data_structures.linked_list.linked_list import LinkedList
from algorithms_and_data_structures.linked_list.merge_sorted_linked_lists import merge_sorted_linked_lists

def test_merge_standard_lists():
    a = LinkedList()
    b = LinkedList()
    for i in [1, 3, 5]: a.append(i)
    for i in [2, 4, 6]: b.append(i)
    
    merged = merge_sorted_linked_lists(a, b)
    assert list(merged) == [1, 2, 3, 4, 5, 6]

def test_merge_different_sizes():
    a = LinkedList()
    b = LinkedList()
    for i in [1, 2]: a.append(i)
    for i in [3, 4, 5, 6]: b.append(i)
    
    merged = merge_sorted_linked_lists(a, b)
    assert list(merged) == [1, 2, 3, 4, 5, 6]

def test_merge_with_duplicates():
    a = LinkedList()
    b = LinkedList()
    for i in [1, 5, 5, 8]: a.append(i)
    for i in [5, 7, 9]: b.append(i)
    
    merged = merge_sorted_linked_lists(a, b)
    assert list(merged) == [1, 5, 5, 5, 7, 8, 9]

def test_merge_with_empty_list():
    empty = LinkedList()
    full = LinkedList()
    for i in [1, 2, 3]: full.append(i)
    
    merged1 = merge_sorted_linked_lists(empty, full)
    assert list(merged1) == [1, 2, 3]
    
    merged2 = merge_sorted_linked_lists(full, empty)
    assert list(merged2) == [1, 2, 3]
    
    merged3 = merge_sorted_linked_lists(empty, empty)
    assert list(merged3) == []

def test_merge_type_error():
    a = LinkedList()
    with pytest.raises(TypeError):
        merge_sorted_linked_lists(a, [1, 2, 3])