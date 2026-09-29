from algorithms_and_data_structures.linked_list.linked_list import LinkedList
from typing import TypeVar

T = TypeVar("T")

def fast_and_slow_pointers(linked_list: LinkedList[T]) -> T:
    if linked_list.is_empty():
        raise ValueError("Cannot find middle of an empty linked list")

    slow = fast = linked_list.head

    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    
    return slow.value