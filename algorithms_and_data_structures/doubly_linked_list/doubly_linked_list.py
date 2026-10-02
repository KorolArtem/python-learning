from typing import Generic, TypeVar, Iterator

T = TypeVar("T")

class _Node(Generic[T]):

    def __init__(self, value: T, prev_node: "_Node[T]" | None = None, next_node: "_Node[T]" | None = None, owner_list: "DoublyLinkedList" = None) -> None:
        self.value: T = value
        self.prev: _Node[T] | None = prev_node
        self.next: _Node[T] | None = next_node 
        self._owner_list : "DoublyLinkedList[T]" | None = owner_list # To be sure we're working with the node of the right list in remove_node(node) of the DoublyLinkedList

    def __repr__(self) -> str:
        return f"Node({self.value})"

class DoublyLinkedList(Generic[T]):

    def __init__(self) -> None:
        
        self._size                  = 0
        self.head: _Node[T] | None  = None
        self.tail: _Node[T] | None  = None

    def _node_at(self, index: int) -> _Node[T]:
        
        if index <= self._size // 2:
            current = self.head
            for _ in range(index):
                current = current.next
        else:
            current = self.tail
            for _ in range(self._size-index-1):
                current = current.prev
        
        return current

    def prepend(self, value: T) -> None:
        
        n = _Node(value=value, owner_list=self)

        if self.head:
            n.next = self.head
            self.head.prev = n
        if not self.tail:
            self.tail = n

        self.head = n
        self._size += 1 

    def append(self, value: T) -> None:

        n = _Node(value=value, owner_list=self)

        if self.tail:
            self.tail.next = n
            n.prev = self.tail
        else:
            self.head = n

        self.tail = n
        self._size += 1

    def remove_node(self, node: _Node[T]) -> T:

        if not isinstance(node, _Node):
            raise TypeError(f"Expected a _Node instance, got {type(node).__name__} instead")
        if node._owner_list is not self:
            raise ValueError("Provided node does not belong to this list")

        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        node._owner_list = None
        node.prev = None
        node.next = None
        self._size -= 1

        return node.value

    def remove(self, value: T) -> None:

        if self._size == 0:
            raise ValueError("This DoublyLinkedList is empty")

        current = self.head

        for _ in range(self._size):
            if current.value == value:
                self.remove_node(current)
                return
            current = current.next

        # I dont really think that I should raise an error when we have an empty list or
        # if the value isnt found. But google says that in python 
        # I should do this, because the built-in list does the same.
        raise ValueError("Value was not found in the list")

    def pop(self, index: int = -1) -> T:

        if not isinstance(index, int):
            raise TypeError(f"Index {index} is invalid")
        if index >= self._size or index < -self._size:
            raise IndexError(f"Index {index} out of range")

        if index < 0:               # Doing this after validating the index so I can show the original index in IndexError()
            index += self._size

        return self.remove_node(self._node_at(index))


    def pop_first(self) -> T:
        
        if self._size == 0:
            raise IndexError("This DoublyLinkedList is empty")

        return self.remove_node(self.head)

    def pop_last(self) -> T:

        if self._size == 0:
            raise IndexError("This DoublyLinkedList is empty")

        return self.remove_node(self.tail)

    def get(self, index: int) -> T:

        if not isinstance(index, int):
            raise TypeError(f"Index {index} is invalid")
        if index >= self._size or index < -self._size:
            raise IndexError(f"Index {index} out of range")

        if index < 0:
            index += self._size

        return self._node_at(index).value

    def find(self, value: T) -> int:

        if self._size == 0:
            raise ValueError(f"{value} is not in the list")

        current = self.head
        for i in range(self._size):
            if current.value == value:
                return i
            current = current.next

        raise ValueError(f"{value} is not in the list")

    def insert(self, index: int, value: T) -> None:

        if not isinstance(index, int):
            raise TypeError(f"Index {index} is invalid")
        if index > self._size or index < -self._size:
            raise IndexError(f"Index {index} out of range")

        if index < 0:
            index += self._size

        if index == 0:
            self.prepend(value)
            return
        elif index == self._size:
            self.append(value)
            return

        current = self._node_at(index)

        n = _Node(value=value, owner_list=self)
        n.prev = current.prev
        n.next = current

        current.prev.next = n
        current.prev = n

        self._size += 1

    def clear(self) -> None:

        current = self.head
        while current is not None:
            next_node = current.next
            current._owner_list = None
            current.prev = None
            current.next = None
            current = next_node

        self.head = None
        self.tail = None
        self._size = 0

    def is_empty(self) -> bool:
        return self.head is None

    def __len__(self) -> int:
        return self._size
    
    def __bool__(self) -> bool:
        return self.head is not None

    def __iter__(self) -> Iterator[T]:
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def __reversed__(self) -> Iterator[T]:
        current = self.tail
        while current is not None:
            yield current.value
            current = current.prev

    def __contains__(self, value: T) -> bool:
        try:
            self.find(value)
            return True
        except ValueError:
            return False
    
    def __getitem__(self, index: int) -> T:
        return self.get(index)

    def __repr__(self) -> str:
        nodes = []
        current = self.head
        while current:
            nodes.append(str(current.value))
            current = current.next
        return " <-> ".join(nodes + ["None"])