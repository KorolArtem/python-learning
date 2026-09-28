from typing import Generic, TypeVar, Iterator

T = TypeVar("T")


class _Node(Generic[T]):

    def __init__(self, value: T, next_node: "_Node[T]" | None = None) -> None:
        self.value: T = value
        self.next: "_Node[T]" | None = next_node

    def __repr__(self) -> str:
        return f"Node({self.value})"

class LinkedList(Generic[T]):

    def __init__(self) -> None:
        self._size: int = 0
        self.head: _Node[T] | None = None
        self.tail: _Node[T] | None = None

    def prepend(self, value: T) -> None:
    
        n = _Node(value)

        if self.head:
            n.next = self.head
        else:
            self.tail = n

        self.head = n
        self._size += 1

    def append(self, value: T) -> None:
        
        n = _Node(value)

        if self.tail:
            self.tail.next = n
        else:
            self.head = n

        self.tail = n
        self._size += 1

    def insert(self, index: int, value: T) -> None:

        if not isinstance(index, int):
            raise TypeError(f"Index {index} is invalid")
        if index < 0: 
            index = self._size + index
        if index > self._size or index < 0:
            raise IndexError(f"Index {index} out of range")
        
        if index == 0:
            self.prepend(value)
            return
        elif index == self._size:
            self.append(value)
            return

        current = self.head
        for _ in range(index - 1):
            current = current.next

        n = _Node(value, current.next)
        current.next = n 
        self._size += 1
        
    def pop_first(self) -> T:

        if self._size == 0:
            raise IndexError("This LinkedList is empty")

        n = self.head
        self.head = self.head.next
        self._size -= 1

        if self._size == 0:
            self.tail = None

        return n.value

    def pop(self, index: int = -1) -> T:

        if not isinstance(index, int):
            raise TypeError(f"Index {index} is invalid")
        if index < 0:
            index = self._size + index
        if index >= self._size or index < 0:
            raise IndexError(f"Index {index} out of range")

        if index == 0:
            return self.pop_first()

        current = self.head
        for _ in range(index-1):
            current = current.next

        if index == self._size - 1:
            self.tail = current

        res = current.next.value

        current.next = current.next.next
        self._size -= 1

        return res

    def remove(self, value: T) -> None:

        if self._size == 0:
            raise ValueError("This LinkedList is empty")
        
        current = self.head
        if current.value == value:
            self.pop_first()
            return
        
        for _ in range(self._size - 1):
            if current.next.value == value:
                if current.next is self.tail:
                    self.tail = current
                
                current.next = current.next.next
                self._size -= 1
                return
            current = current.next
                
        raise ValueError("Value was not found in the list")

    def clear(self) -> None:
        self.head = None
        self.tail = None
        self._size = 0

    def get(self, index: int) -> T:

        if not isinstance(index, int):
            raise TypeError(f"Index {index} is invalid")
        if index < 0:
            index = self._size + index
        if index >= self._size or index < 0:
            raise IndexError(f"Index {index} out of range")

        if index == 0:
            return self.head.value
        
        current = self.head
        for _ in range(index):
            current = current.next

        return current.value

    def find(self, value: T) -> int | None:

        if self._size == 0:
            return None

        current = self.head
        for i in range(self._size):
            if current.value == value:
                return i
            current = current.next

        return None

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

    def __contains__(self, value: T) -> bool:
        return self.find(value) is not None 
    
    def __getitem__(self, index: int) -> T:
        return self.get(index)

    def __repr__(self) -> str:
        nodes = []
        current = self.head
        while current:
            nodes.append(str(current.value))
            current = current.next
        return " -> ".join(nodes + ["None"])