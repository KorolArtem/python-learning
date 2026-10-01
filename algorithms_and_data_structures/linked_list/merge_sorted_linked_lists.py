from algorithms_and_data_structures.linked_list.linked_list import LinkedList
from typing import TypeVar

T = TypeVar("T")

def merge_sorted_linked_lists(a: LinkedList[T], b: LinkedList[T]) -> LinkedList[T]:
    
    if a is None or b is None:
        raise ValueError("Something wrong with your lists")
    if not isinstance(a, LinkedList) or not isinstance(b, LinkedList):
        raise TypeError("Both arguments must be of type LinkedList")

    a_next = a.head
    b_next = b.head

    result = LinkedList[T]()

    while a_next or b_next:
        if a_next and b_next:                   # both are not empty
            if a_next.value >= b_next.value:
                result.append(b_next.value)
                b_next = b_next.next
            else:
                result.append(a_next.value)
                a_next = a_next.next
        else:                                   # one or both are empty
            if a_next:                          # only b is empty
                result.append(a_next.value)
                a_next = a_next.next
            elif b_next:                        # only a is empty
                result.append(b_next.value)
                b_next = b_next.next

    return result

if __name__ == "__main__":
    a = LinkedList()
    # a.append(1)
    # a.append(5)
    # a.append(9)

    b = LinkedList()
    b.append(3)
    b.append(4)
    b.append(6)
    b.append(8)

    r = merge_sorted_linked_lists(a, b)
    print(r)