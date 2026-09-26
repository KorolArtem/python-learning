from typing import Any

#Default stack
class Stack:
    
    def __init__(self) -> None:
        self._stack = []

    def push(self, item: Any) -> None:
        self._stack.append(item)

    def top(self) -> Any:
        if self._stack: return self._stack[-1]
        else: raise IndexError("This stack is empty")

    def pop(self) -> Any:
        if self._stack: return self._stack.pop()
        else: raise IndexError("This stack is empty")

    def is_empty(self) -> bool:
        return len(self._stack) == 0

    def clear(self) -> None:
        self._stack = []