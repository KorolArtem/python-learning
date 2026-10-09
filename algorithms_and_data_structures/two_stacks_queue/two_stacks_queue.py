from algorithms_and_data_structures.stack.stack import Stack
from collections.abc import Iterator # Okay, typing is outdated, I know this now...

class Queue[T]:

    def __init__(self, data: list[T] | T | None = None) -> None:

        self._in_stack : Stack[T] = Stack()
        self._out_stack : Stack[T] = Stack()

        if data is not None:
            items = data if isinstance(data, list) else [data]

            for item in items:
                self.enqueue(item)

    def enqueue(self, item: T) -> None:

        self._in_stack.push(item)
        
    def _transfer_elements(self) -> None:

        if self._out_stack.is_empty():
            while not self._in_stack.is_empty():
                self._out_stack.push(self._in_stack.pop())

    def is_empty(self) -> bool:

        return self._out_stack.is_empty() and self._in_stack.is_empty()
    
    def dequeue(self) -> T:

        if self.is_empty():
            raise IndexError("This queue is empty")

        self._transfer_elements()

        return self._out_stack.pop()

    def peek(self) -> T:

        if self.is_empty():
            raise IndexError("This queue is empty")

        self._transfer_elements()

        return self._out_stack.top()

    def __len__(self) -> int:

        return len(self._in_stack) + len(self._out_stack)

    def __bool__(self) -> bool:

        return len(self) > 0

    def __iter__(self) -> Iterator[T]:

        yield from self._out_stack
        yield from reversed(list(self._in_stack))

    def __str__(self) -> str:

        return "Queue(" + " -> ".join(str(item) for item in self) + ")"

    def __repr__(self) -> str:
        return f"Queue(in_stack_size={len(self._in_stack)}, out_stack_size={len(self._out_stack)})"