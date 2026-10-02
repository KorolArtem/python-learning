from collections.abc import Iterator

#Default stack
class Stack[T]: # I only just found out they added that syntactic sugar in the new versions.

    def __init__(self) -> None:

        self._stack: list[T] = []

    def push(self, item: T) -> None:

        self._stack.append(item)

    def top(self) -> T:

        if self._stack: 
            return self._stack[-1]
        else: 
            raise IndexError("This stack is empty")

    def pop(self) -> T:

        if self._stack: 
            return self._stack.pop()
        else: 
            raise IndexError("This stack is empty")

    def is_empty(self) -> bool:

        return len(self._stack) == 0

    def clear(self) -> None:

        self._stack.clear()

    def __len__(self) -> int:

        return len(self._stack)

    def __iter__(self) -> Iterator[T]:

        return reversed(self._stack)