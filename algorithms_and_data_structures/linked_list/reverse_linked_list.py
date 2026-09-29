from algorithms_and_data_structures.linked_list.linked_list import LinkedList

def reverse_linked_list(linked_list: LinkedList) -> LinkedList:
    if len(linked_list) == 0: 
        return linked_list

    previous_node = None
    current_node = linked_list.head

    linked_list.tail = linked_list.head

    while current_node is not None:
        next_node = current_node.next
        current_node.next = previous_node

        previous_node = current_node
        current_node = next_node

    linked_list.head = previous_node
    
    return linked_list